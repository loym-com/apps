odoo.define('pos_worldline.payment', function (require) {
    "use strict";

    var core = require('web.core');
    var rpc = require('web.rpc');
    var PaymentInterface = require('point_of_sale.PaymentInterface');
    const { Gui } = require('point_of_sale.Gui');

    var _t = core._t;

    var PaymentWorldline = PaymentInterface.extend({
        send_payment_request: function (cid) {
            this._super.apply(this, arguments);
            this._reset_state();
            return this._worldline_pay(cid);
        },
        send_payment_cancel: function (order, cid) {
            this._super.apply(this, arguments);
            return this._worldline_cancel();
        },
        close: function () {
            this._super.apply(this, arguments);
        },

        set_most_recent_service_id(id) {
            this.most_recent_service_id = id;
        },

        pending_worldline_line() {
          return this.pos.get_order().paymentlines.find(
            paymentLine => paymentLine.payment_method.use_payment_terminal === 'worldline' && (!paymentLine.is_done()));
        },

        // private methods
        _reset_state: function () {
            this.was_cancelled = false;
            this.remaining_polls = 4;
            clearTimeout(this.polling);
        },

        _handle_odoo_connection_failure: function (data) {
            // handle timeout
            var line = this.pending_worldline_line();
            if (line) {
                line.set_payment_status('retry');
            }
            this._show_error(_t('Could not connect to the Odoo server, please check your internet connection and try again.'));

            return Promise.reject(data); // prevent subsequent onFullFilled's from being called
        },

        _call_worldline: function (data, operation) {
            return rpc.query({
                model: 'pos.payment.method',
                method: 'proxy_worldline_request',
                args: [[this.payment_method.id], data, operation],
            }, {
                // When a payment terminal is disconnected it may take Worldline
                // a while to return an error (Adyen: ~6s). So wait 10 seconds
                // before concluding Odoo is unreachable.
                timeout: 30000, // Wait longer for immediate payment (not async)
                shadow: true,
            }).catch(this._handle_odoo_connection_failure.bind(this));
        },

        _worldline_get_sale_id: function () {
            var config = this.pos.config;
            return _.str.sprintf('%s (ID: %s)', config.display_name, config.id);
        },

        // _worldline_common_message_header: function () {
        //     var config = this.pos.config;
        //     this.most_recent_service_id = Math.floor(Math.random() * Math.pow(2, 64)).toString(); // random ID to identify request/response pairs
        //     this.most_recent_service_id = this.most_recent_service_id.substring(0, 10); // max length is 10

        //     return {
        //         'ProtocolVersion': '3.0',
        //         'MessageClass': 'Service',
        //         'MessageType': 'Request',
        //         'SaleID': this._worldline_get_sale_id(config),
        //         'ServiceID': this.most_recent_service_id,
        //         'POIID': this.payment_method.worldline_terminal_identifier
        //     };
        // },

        _worldline_pay_data: function () {
            var order = this.pos.get_order();
            var config = this.pos.config;
            var line = order.selected_paymentline;
            var pow = Math.pow(10, this.pos.currency.decimal_places);
            var data = {
                "payload": {
                    "amounts": {
                        "currencySymbol": this.pos.currency.name,
                        // "base": Math.round(line.amount * pow) / pow,
                        "base": line.amount
                    }
                }
            }
            return data;
        },

        _worldline_pay: function (cid) {
            var self = this;
            var order = this.pos.get_order();

            if (order.selected_paymentline.amount < 0) {
                this._show_error(_t('Cannot process transactions with negative amount.'));
                return Promise.resolve();
            }

            if (order === this.poll_error_order) {
                delete this.poll_error_order;
                return self._worldline_handle_response({});
            }

            var data = this._worldline_pay_data();
            var line = order.paymentlines.find(paymentLine => paymentLine.cid === cid);
            return this._call_worldline(data, "Payments").then(function (data) {
                return self._worldline_handle_response(data, "Payments");
            });
        },

        // _worldline_cancel: function (ignore_error) {
        //     var self = this;
        //     var config = this.pos.config;
        //     var previous_service_id = this.most_recent_service_id;
        //     var header = _.extend(this._worldline_common_message_header(), {
        //         'MessageCategory': 'Abort',
        //     });

        //     var data = {};

        //     return this._call_worldline(data, OPERATION).then(function (data) {
        //         // Only valid response is a 200 OK HTTP response which is
        //         // represented by true.
        //         if (! ignore_error && data !== true) {
        //             self._show_error(_t('Cancelling the payment failed. Please cancel it manually on the payment terminal.'));
        //             self.was_cancelled = !!self.polling;
        //         }
        //     });
        // },

        // _convert_receipt_info: function (output_text) {
        //     return output_text.reduce(function (acc, entry) {
        //         var params = new URLSearchParams(entry.Text);

        //         if (params.get('name') && !params.get('value')) {
        //             return acc + _.str.sprintf('<br/>%s', params.get('name'));
        //         } else if (params.get('name') && params.get('value')) {
        //             return acc + _.str.sprintf('<br/>%s: %s', params.get('name'), params.get('value'));
        //         }

        //         return acc;
        //     }, '');
        // },

        // _poll_for_response: function (resolve, reject) {
        //     var self = this;
        //     if (this.was_cancelled) {
        //         resolve(false);
        //         return Promise.resolve();
        //     }

        //     return rpc.query({
        //         model: 'pos.payment.method',
        //         method: 'get_latest_worldline_status',
        //         args: [[this.payment_method.id], this._worldline_get_sale_id()],
        //     }, {
        //         timeout: 5000,
        //         shadow: true,
        //     }).catch(function (data) {
        //         if (self.remaining_polls != 0) {
        //             self.remaining_polls--;
        //         } else {
        //             reject();
        //             self.poll_error_order = self.pos.get_order();
        //             return self._handle_odoo_connection_failure(data);
        //         }
        //         // This is to make sure that if 'data' is not an instance of Error (i.e. timeout error),
        //         // this promise don't resolve -- that is, it doesn't go to the 'then' clause.
        //         return Promise.reject(data);
        //     }).then(function (status) {
        //         var notification = status.latest_response;
        //         var order = self.pos.get_order();
        //         var line = self.pending_worldline_line() || resolve(false);

        //         if (notification && notification.SaleToPOIResponse.MessageHeader.ServiceID == line.terminalServiceId) {
        //             var response = notification.SaleToPOIResponse.PaymentResponse.Response;
        //             var additional_response = new URLSearchParams(response.AdditionalResponse);

        //             if (response.Result == 'Success') {
        //                 var config = self.pos.config;
        //                 var payment_response = notification.SaleToPOIResponse.PaymentResponse;
        //                 var payment_result = payment_response.PaymentResult;

        //                 var cashier_receipt = payment_response.PaymentReceipt.find(function (receipt) {
        //                     return receipt.DocumentQualifier == 'CashierReceipt';
        //                 });

        //                 if (cashier_receipt) {
        //                     line.set_cashier_receipt(self._convert_receipt_info(cashier_receipt.OutputContent.OutputText));
        //                 }

        //                 var customer_receipt = payment_response.PaymentReceipt.find(function (receipt) {
        //                     return receipt.DocumentQualifier == 'CustomerReceipt';
        //                 });

        //                 if (customer_receipt) {
        //                     line.set_receipt_info(self._convert_receipt_info(customer_receipt.OutputContent.OutputText));
        //                 }

        //                 var tip_amount = payment_result.AmountsResp.TipAmount;
        //                 if (config.worldline_ask_customer_for_tip && tip_amount > 0) {
        //                     order.set_tip(tip_amount);
        //                     line.set_amount(payment_result.AmountsResp.AuthorizedAmount);
        //                 }

        //                 line.transaction_id = additional_response.get('pspReference');
        //                 line.card_type = additional_response.get('cardType');
        //                 line.cardholder_name = additional_response.get('cardHolderName') || '';
        //                 resolve(true);
        //             } else {
        //                 var message = additional_response.get('message');
        //                 self._show_error(_.str.sprintf(_t('Message from Worldline: %s'), message));

        //                 // this means the transaction was cancelled by pressing the cancel button on the device
        //                 if (message.startsWith('108 ')) {
        //                     resolve(false);
        //                 } else {
        //                     line.set_payment_status('retry');
        //                     reject();
        //                 }
        //             }
        //         } else {
        //             line.set_payment_status('waitingCard')
        //         }
        //     });
        // },

        _worldline_handle_response: function (response, operation) {
            var line = this.pending_worldline_line();

            if (response.error && response.error.status_code == 401) {
                this._show_error(_t('Authentication failed. Please check your Worldline credentials.'));
                line.set_payment_status('force_done');
                return Promise.resolve();
            }

            if (response && response.transactionOutcome in ["Declined", "Cancelled"]) {
                console.error('error from Worldline', response);

                this._show_error(_.str.sprintf(
                    _t('The transaction was %s'),
                    response.transactionOutcome.toLowerCase()
                ));
                if (line) {
                    line.set_payment_status('force_done');
                }

                return Promise.resolve();
            } else if (operation == "Payments") {
                // Approved
                line.ticket = response.receipt.customer.plain // or escpos
                return true // What to return?
            // } else if (operation == "PaymentsAsync") {
            //     // Approved
            //     line.set_payment_status('waitingCard');
            //     return this.start_get_status_polling()
            }
        },

        // start_get_status_polling() {
        //     var self = this;
        //     var res = new Promise(function (resolve, reject) {
        //         // clear previous intervals just in case, otherwise
        //         // it'll run forever
        //         clearTimeout(self.polling);
        //         self._poll_for_response(resolve, reject);
        //         self.polling = setInterval(function () {
        //             self._poll_for_response(resolve, reject);
        //         }, 5500);
        //     });

        //     // make sure to stop polling when we're done
        //     res.finally(function () {
        //         self._reset_state();
        //     });

        //     return res;
        // },

        _show_error: function (msg, title) {
            if (!title) {
                title =  _t('Worldline Error');
            }
            Gui.showPopup('ErrorPopup',{
                'title': title,
                'body': msg,
            });
        },
    });

    return PaymentWorldline;
});

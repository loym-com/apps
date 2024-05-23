odoo.define('pos_worldline.payment', function (require) {
    "use strict";

    var core = require('web.core');
    var rpc = require('web.rpc');
    var PaymentInterface = require('point_of_sale.PaymentInterface');
    const { Gui } = require('point_of_sale.Gui');

    var _t = core._t;

    // BASED ON PaymentAdyen
    var PaymentWorldline = PaymentInterface.extend({
        send_payment_request: function (cid) {
            this._super.apply(this, arguments);
            this._reset_state();
            return this._worldline_pay(cid);
        },
        // send_payment_cancel: function (order, cid) {
        //     this._super.apply(this, arguments);
        //     return this._worldline_cancel();
        // },
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

        _handle_odoo_connection_failure: function (response) {
            // handle timeout
            var line = this.pending_worldline_line();
            if (line) {
                line.set_payment_status('retry');
            }

            this._show_error(_t('Could not connect to the Odoo server, please check your internet connection and try again.'));

            return Promise.reject(data); // prevent subsequent onFullFilled's from being called
        },

        _call_worldline: function (data) {
            return rpc.query({
                model: 'pos.payment.method',
                method: 'worldline_do_payment',
                args: [[this.payment_method.id], data],
            }, {
                // When a payment terminal is disconnected it may take Worldline
                // a while to return an error (Adyen: ~6s). So wait 10 seconds
                // before concluding Odoo is unreachable.
                // FIXME: Timeout ERROR -> must delete the POS order and register again.
                timeout: 60000,
                shadow: true,
            }).catch(
                this._handle_odoo_connection_failure.bind(this)
            );
        },

        _worldline_get_sale_id: function () {
            var config = this.pos.config;
            return _.str.sprintf('%s (ID: %s)', config.display_name, config.id);
        },

        _worldline_pay_data: function (cid) {
            var order = this.pos.get_order();
            var config = this.pos.config;
            var line = order.selected_paymentline;
            var data = {
                "amounts": {
                    "currencySymbol": this.pos.currency.name,
                    "base": line.amount
                },
                "cashierId": config.id,
                "customData": {
                    "client_id": cid,
                },
            };
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

            var data = this._worldline_pay_data(cid);
            var line = order.paymentlines.find(paymentLine => paymentLine.cid === cid);
            return this._call_worldline(data).then(function (data) {
                return self._worldline_handle_response(data, "Payments");
            });
        },

        _worldline_handle_response: function (responseJSON, operation) {
            var response = JSON.parse(responseJSON);

            var line = this.pending_worldline_line();

            if ('status_code' in response) {
                if (response.status_code == 400) {
                    this._show_error(_t("Bad request. Please check your Worldline credentials."));
                    line.set_payment_status('retry');
                    return Promise.resolve();
                }
                else if (response.status_code == 401) {
                    this._show_error(_t("Authentication failed. Please check your Worldline credentials."));
                    line.set_payment_status('retry');
                    return Promise.resolve();
                }
                // else if (response.status_code == 404) {
                //     // Payments/latest first time after "dagsoppgjør"
                // }
                else if (response.status_code == 503) {
                    this._show_error(_t("The terminal was busy and did not process your request. Please try again."));
                    line.set_payment_status('retry');
                    return Promise.resolve();
                }
                else {
                    this._show_error(_t(response.error.status_code + ' ' + response.error.message));
                    line.set_payment_status('retry');
                    return Promise.resolve();
                }
            }

            // Response 200 OK

            if (response && ["Declined", "Cancelled"].includes(response.transactionOutcome)) {

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
            }
        },

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

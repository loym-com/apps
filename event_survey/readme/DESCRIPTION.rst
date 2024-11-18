Successful event survey implementation depends on

0) User Settings
Manage Event Registration with Survey

1) Survey
Create the survey
On the event, select the survey

2) Mail Template
Admin Mail Templates: 'Event: Registration': Duplicate and add a link to the survey: ${object.survey_user_input_id.fill_url}
On the event email schedule, select the mail template

2019: NEW WORKFLOW

BUG: Create new ticket -> registration_ticket_question_id is set to False!

2021
On the company, configure a Technical User. The user must have sufficient rights (event, survey & sales?).
Create a PRODUCT for each ticket (optional).
Create an event PARTNER (optional). Must be active. The country must be set.
Create the SURVEY:
- Name - Single Line Text Box - Mandatory
- Email - Single Line Text Box - Mandatory - Input must be an email.
- Phone - Single Line Text Box
- Ticket - Multiple choice: only one answer - Mandatory - DO NOT select the product for each ticket.
- Survey Action after survey: After survey go to event registration survey list
Create the EVENT:
- Select registration survey, partner (optional), name, email, phone, ticket.
- Create tickets. For each ticket, set price = 0 and select a survey ticket.
- 16.0: Set state = Advertized (?)
FYI:
- The product name and the ticket & event display names are written on the sales order.
BUGS:
(Tested in 12.0 as public user, not logged in.)
- In the end, the cart is not emptied!
- The partner being used is the admin? or technical_user? instead of the event_partner.
- The public user can change the partner contact info!

# cr-invoices
test project

BACKEND


--main code is in invoices/invoices.py--

Dependencies:
  Python, Flask
  

Install invoices app:
  1. move to application root directory
  2. execute: pip install --editable .
  3. execute (on linux): export FLASK_APP=invoices
  3. execute (on win): set FLASK_APP=invoices
  4. execute: flask run

Flask app should now be running on localhost:5000



API endpoints:

Get list of all invoices:

    localhost:5000/invoices/

    curl -i http://localhost:5000/invoices

Get one invoice:

    localhost:5000/invoices/[invoice_id]

    curl -i http://localhost:5000/invoices/[id]
    curl -i http://localhost:5000/invoices/3

Create invoice:

    localhost:5000/invoices POST

    curl -i -H "Content-Type: application/json" -X POST -d '{"customer":"klemen","total":200}' http://localhost:5000/invoices 

Update invoice:

    localhost:5000/invoices/[invoice_id] PUT

    curl -i -H "Content-Type: application/json" -X PUT -d '{"customer":"new","total":600}' http://localhost:5000/invoices/1

Delete invoice:

    localhost:5000/invoices/[invoice_id] DELETE

    curl -X DELETE http://localhost:5000/invoices/1





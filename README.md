Motivation
----------

This program is used to create tree like money reports.

Usage
-----

First, build a json file of the form:

    :::json
    {
        "Income":
        {
            "currency": "USD",
            "inner":
            {
                "SomeBusiness":
                {
                    "1": 1544.32,
                    "2": 2105.11
                },
                "OtherThing": 50.12
            }
        },
        "Expenses":
        {
            "Business": 
            {
                "SomeExpense": 
                {
                    "currency": "USD",
                    "inner": 
                    {
                        "1": 30,
                        "2": 30
                    }
                },
                "SomethingElse2":
                {
                    "currency": "USD",
                    "inner": 54.3
                },
                "OtherExpense":
                {
                    "currency": "USD",
                    "inner": 
                    {
                        "1": 15,
                        "2": 15
                    }
                },
                "MoreExpense":
                {
                    "currency": "USD",
                    "inner":
                    {
                        "1":10.19,
                        "2":15.75
                    }
                },
                "OtherThing":
                {
                    "currency": "EUR",
                    "inner": 145.08
                }
            },
            "Bills":
            {
                "currency": "EUR",
                "inner": 
                {
                    "Water": 60.10,
                    "Electricity": 71.18
                }
            }
        }
    }

Next, run:

    runreport yourfile.json

This is the expected output:

    Expenses : 276.36 EUR, 170.24 USD
        Bills : 131.28 EUR
            Electricity : 71.18 EUR
            Water : 60.10 EUR
        Business : 145.08 EUR, 170.24 USD
            MoreExpense : 25.94 USD
                1 : 10.19 USD
                2 : 15.75 USD
            OtherExpense : 30.00 USD
                1 : 15.00 USD
                2 : 15.00 USD
            OtherThing : 145.08 EUR
            SomeExpense : 60.00 USD
                1 : 30.00 USD
                2 : 30.00 USD
            SomethingElse2 : 54.30 USD
    Income : 3699.55 USD
        OtherThing : 50.12 USD
        SomeBusiness : 3649.43 USD
            1 : 1544.32 USD
            2 : 2105.11 USD





# data for adding sample bills to MySQL database
def sample_bills():
    bill_list = [
        {
            'spending_0': 12.12,
            'spending_1': 14.78,
            'date': '2018-04-23',
            'restaurant': 'Seto',
            'notes': 'sushi was good',
            'who_paid': 0
        },
        {
            'spending_0': 17.29,
            'spending_1': 16.87,
            'date': '2018-04-29',
            'restaurant': 'Falafel House',
            'notes': 'crispy falafels',
            'who_paid': 1
        },
        {
            'spending_0': 9.23,
            'spending_1': 10.98,
            'date': '2018-05-02',
            'restaurant': 'Whole Foods',
            'notes': 'quick lunch',
            'who_paid': 0
        },
        {
            'spending_0': 25.24,
            'spending_1': 27.28,
            'date': '2018-05-06',
            'restaurant': 'Benihana',
            'notes': 'anniversary date',
            'who_paid': 1
        },
        {
            'spending_0': 13.14,
            'spending_1': 14.20,
            'date': '2018-05-03',
            'restaurant': 'Pizza Kitchen',
            'notes': 'great mushrooms',
            'who_paid': 0
        }
    ]
    return bill_list

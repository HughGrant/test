VOLTAGE_CHOICES = (
    (0, '无电压'),
    (220, '220V'),
    (110, '110V'),
)

SOCKET_CHOICES = (
    (0, '国标'),
    (1, '英标'),
    (2, '美标'),
    (3, '意标'),
    (4, '南非标'),
    (5, '瑞士标'),
    (6, '欧标(德标)'),
)

CURRENCY_TYPE = (
    ('US', 'USD'),
    ('CH', 'RMB'),
    ('EU', 'EUR'),
    ('GB', 'GBP'),
    ('JP', 'JPY'),
    ('AU', 'AUD'),
    ('CA', 'CAD'),
    ('CF', 'CHF'),
    ('NT', 'NTD'),
    ('HK', 'HKD'),
    ('NZ', 'NZD'),
    ('OT', 'Other'),
)

PAYMENT_METHOD = (
    (0, '未付款'),
    (1, 'PAYPAL'),
    (2, '西联'),
    (3, 'T/T'),
    (4, '国内银行转账'),
)

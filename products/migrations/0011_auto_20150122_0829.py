# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_extend_is_markdown'),
    ]

    operations = [
        migrations.CreateModel(
            name='MOQ',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('min_order_quantity', models.IntegerField(default=1, verbose_name='起订量')),
                ('min_order_unit', models.IntegerField(default=20, verbose_name='起订单位', choices=[(26, 'Acre/Acres'), (27, 'Ampere/Amperes'), (1, 'Bag/Bags'), (19, 'Barrel/Barrels'), (91, 'Blade/Blades'), (28, 'Box/Boxes'), (18, 'Bushel/Bushels'), (90, 'Carat/Carats'), (29, 'Carton/Cartons'), (30, 'Case/Cases'), (31, 'Centimeter/Centimeters'), (32, 'Chain/Chains'), (92, 'Combo/Combos'), (33, 'Cubic Centimeter/Cubic Centimeters'), (34, 'Cubic Foot/Cubic Feet'), (35, 'Cubic Inch/Cubic Inches'), (13, 'Cubic Meter/Cubic Meters'), (36, 'Cubic Yard/Cubic Yards'), (37, 'Degrees Celsius'), (38, 'Degrees Fahrenheit'), (14, 'Dozen/Dozens'), (39, 'Dram/Drams'), (40, 'Fluid Ounce/Fluid Ounces'), (41, 'Foot/Feet'), (88, 'Forty-Foot Container'), (42, 'Furlong/Furlongs'), (15, 'Gallon/Gallons'), (43, 'Gill/Gills'), (44, 'Grain/Grains'), (17, 'Gram/Grams'), (87, 'Gross'), (45, 'Hectare/Hectares'), (46, 'Hertz'), (47, 'Inch/Inches'), (48, 'Kiloampere/Kiloamperes'), (16, 'Kilogram/Kilograms'), (49, 'Kilohertz'), (10, 'Kilometer/Kilometers'), (50, 'Kiloohm/Kiloohms'), (51, 'Kilovolt/Kilovolts'), (52, 'Kilowatt/Kilowatts'), (22, 'Liter/Liters'), (9, 'Long Ton/Long Tons'), (53, 'Megahertz'), (8, 'Meter/Meters'), (7, 'Metric Ton/Metric Tons'), (54, 'Mile/Miles'), (55, 'Milliampere/Milliamperes'), (24, 'Milligram/Milligrams'), (56, 'Millihertz'), (57, 'Milliliter/Milliliters'), (58, 'Millimeter/Millimeters'), (59, 'Milliohm/Milliohms'), (60, 'Millivolt/Millivolts'), (61, 'Milliwatt/Milliwatts'), (62, 'Nautical Mile/Nautical Miles'), (63, 'Ohm/Ohms'), (6, 'Ounce/Ounces'), (21, 'Pack/Packs'), (5, 'Pair/Pairs'), (86, 'Pallet/Pallets'), (64, 'Parcel/Parcels'), (65, 'Perch/Perches'), (4, 'Piece/Pieces'), (66, 'Pint/Pints'), (85, 'Plant/Plants'), (67, 'Pole/Poles'), (3, 'Pound/Pounds'), (68, 'Quart/Quarts'), (69, 'Quarter/Quarters'), (70, 'Rod/Rods'), (71, 'Roll/Rolls'), (20, 'Set/Sets'), (89, 'Sheet/Sheets'), (2, 'Short Ton/Short Tons'), (72, 'Square Centimeter/Square Centimeters'), (73, 'Square Foot/Square Feet'), (74, 'Square Inch/Square Inches'), (12, 'Square Meter/Square Meters'), (75, 'Square Mile/Square Miles'), (76, 'Square Yard/Square Yards'), (77, 'Stone/Stones'), (84, 'Strand/Strands'), (11, 'Ton/Tons'), (78, 'Tonne/Tonnes'), (79, 'Tray/Trays'), (83, 'Twenty-Foot Container'), (25, 'Unit/Units'), (80, 'Volt/Volts'), (81, 'Watt/Watts'), (82, 'Wp'), (23, 'Yard/Yards')])),
            ],
            options={
                'verbose_name': '最小起订量',
                'verbose_name_plural': '最小起订量',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='minorderquantity',
            name='extend',
        ),
        migrations.DeleteModel(
            name='MinOrderQuantity',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='extend',
        ),
        migrations.DeleteModel(
            name='PaymentMethod',
        ),
        migrations.AlterModelOptions(
            name='supplyability',
            options={'verbose_name': '供贷能力', 'verbose_name_plural': '供贷能力'},
        ),
        migrations.RemoveField(
            model_name='fobprice',
            name='extend',
        ),
        migrations.RemoveField(
            model_name='supplyability',
            name='extend',
        ),
        migrations.AddField(
            model_name='extend',
            name='fob_price',
            field=models.ForeignKey(default='', verbose_name='FOB报价', to='products.FobPrice'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extend',
            name='moq',
            field=models.ForeignKey(default=0, verbose_name='最小起订量', to='products.MOQ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extend',
            name='payment_terms',
            field=models.CharField(max_length=200, verbose_name='付款方式', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extend',
            name='supply_ability',
            field=models.ForeignKey(default=0, verbose_name='供贷能力', to='products.SupplyAbility'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20150114_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称', choices=[('PayPal', 'PayPal'), ('Western Union', 'Western Union'), ('T/T', 'T/T'), ('L/C', 'L/C'), ('D/A', 'D/A'), ('D/P', 'D/P'), ('MoneyGram', 'MoneyGram')])),
                ('extend', models.ForeignKey(to='products.Extend', verbose_name='产品详细信息')),
            ],
            options={
                'verbose_name_plural': '付款方式',
                'verbose_name': '付款方式',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('url', models.CharField(verbose_name='图片来源', max_length=300)),
                ('extend', models.ForeignKey(to='products.Extend', verbose_name='产品详细信息')),
            ],
            options={
                'verbose_name_plural': '产品图片',
                'verbose_name': '产品图片',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='minorderquantity',
            options={'verbose_name_plural': '最小起订量', 'verbose_name': '最小起订量'},
        ),
        migrations.AddField(
            model_name='extend',
            name='url',
            field=models.CharField(blank=True, verbose_name='产品来源', max_length=300),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='cn_name',
            field=models.CharField(blank=True, verbose_name='中文名', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='size',
            field=models.CharField(blank=True, verbose_name='尺寸(CM)', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='voltage',
            field=models.IntegerField(default=0, verbose_name='电压', choices=[(0, '无电压'), (220, '220V'), (110, '110V')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fobprice',
            name='price_uint',
            field=models.IntegerField(default=20, verbose_name='报价单位', choices=[(26, 'Acre'), (27, 'Ampere'), (1, 'Bag'), (19, 'Barrel'), (91, 'Blade'), (28, 'Box'), (18, 'Bushel'), (90, 'Carat'), (29, 'Carton'), (30, 'Case'), (31, 'Centimeter'), (32, 'Chain'), (92, 'Combo'), (33, 'Cubic Centimeter'), (34, 'Cubic Foot'), (35, 'Cubic Inch'), (13, 'Cubic Meter'), (36, 'Cubic Yard'), (14, 'Dozen'), (39, 'Dram'), (40, 'Fluid Ounce'), (41, 'Foot'), (42, 'Furlong'), (15, 'Gallon'), (43, 'Gill'), (44, 'Grain'), (17, 'Gram'), (45, 'Hectare'), (47, 'Inch'), (48, 'Kiloampere'), (16, 'Kilogram'), (10, 'Kilometer'), (50, 'Kiloohm'), (51, 'Kilovolt'), (52, 'Kilowatt'), (22, 'Liter'), (9, 'Long Ton'), (8, 'Meter'), (7, 'Metric Ton'), (54, 'Mile'), (55, 'Milliampere'), (24, 'Milligram'), (57, 'Milliliter'), (58, 'Millimeter'), (59, 'Milliohm'), (60, 'Millivolt'), (61, 'Milliwatt'), (62, 'Nautical Mile'), (63, 'Ohm'), (6, 'Ounce'), (21, 'Pack'), (5, 'Pair'), (86, 'Pallet'), (64, 'Parcel'), (65, 'Perch'), (4, 'Piece'), (66, 'Pint'), (85, 'Plant'), (67, 'Pole'), (3, 'Pound'), (68, 'Quart'), (69, 'Quarter'), (70, 'Rod'), (71, 'Roll'), (20, 'Set'), (89, 'Sheet'), (2, 'Short Ton'), (72, 'Square Centimeter'), (73, 'Square Foot'), (74, 'Square Inch'), (12, 'Square Meter'), (75, 'Square Mile'), (76, 'Square Yard'), (77, 'Stone'), (84, 'Strand'), (11, 'Ton'), (78, 'Tonne'), (79, 'Tray'), (25, 'Unit'), (80, 'Volt'), (81, 'Watt'), (23, 'Yard')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='minorderquantity',
            name='min_order_unit',
            field=models.IntegerField(default=20, verbose_name='起订单位', choices=[(26, 'Acre/Acres'), (27, 'Ampere/Amperes'), (1, 'Bag/Bags'), (19, 'Barrel/Barrels'), (91, 'Blade/Blades'), (28, 'Box/Boxes'), (18, 'Bushel/Bushels'), (90, 'Carat/Carats'), (29, 'Carton/Cartons'), (30, 'Case/Cases'), (31, 'Centimeter/Centimeters'), (32, 'Chain/Chains'), (92, 'Combo/Combos'), (33, 'Cubic Centimeter/Cubic Centimeters'), (34, 'Cubic Foot/Cubic Feet'), (35, 'Cubic Inch/Cubic Inches'), (13, 'Cubic Meter/Cubic Meters'), (36, 'Cubic Yard/Cubic Yards'), (37, 'Degrees Celsius'), (38, 'Degrees Fahrenheit'), (14, 'Dozen/Dozens'), (39, 'Dram/Drams'), (40, 'Fluid Ounce/Fluid Ounces'), (41, 'Foot/Feet'), (88, 'Forty-Foot Container'), (42, 'Furlong/Furlongs'), (15, 'Gallon/Gallons'), (43, 'Gill/Gills'), (44, 'Grain/Grains'), (17, 'Gram/Grams'), (87, 'Gross'), (45, 'Hectare/Hectares'), (46, 'Hertz'), (47, 'Inch/Inches'), (48, 'Kiloampere/Kiloamperes'), (16, 'Kilogram/Kilograms'), (49, 'Kilohertz'), (10, 'Kilometer/Kilometers'), (50, 'Kiloohm/Kiloohms'), (51, 'Kilovolt/Kilovolts'), (52, 'Kilowatt/Kilowatts'), (22, 'Liter/Liters'), (9, 'Long Ton/Long Tons'), (53, 'Megahertz'), (8, 'Meter/Meters'), (7, 'Metric Ton/Metric Tons'), (54, 'Mile/Miles'), (55, 'Milliampere/Milliamperes'), (24, 'Milligram/Milligrams'), (56, 'Millihertz'), (57, 'Milliliter/Milliliters'), (58, 'Millimeter/Millimeters'), (59, 'Milliohm/Milliohms'), (60, 'Millivolt/Millivolts'), (61, 'Milliwatt/Milliwatts'), (62, 'Nautical Mile/Nautical Miles'), (63, 'Ohm/Ohms'), (6, 'Ounce/Ounces'), (21, 'Pack/Packs'), (5, 'Pair/Pairs'), (86, 'Pallet/Pallets'), (64, 'Parcel/Parcels'), (65, 'Perch/Perches'), (4, 'Piece/Pieces'), (66, 'Pint/Pints'), (85, 'Plant/Plants'), (67, 'Pole/Poles'), (3, 'Pound/Pounds'), (68, 'Quart/Quarts'), (69, 'Quarter/Quarters'), (70, 'Rod/Rods'), (71, 'Roll/Rolls'), (20, 'Set/Sets'), (89, 'Sheet/Sheets'), (2, 'Short Ton/Short Tons'), (72, 'Square Centimeter/Square Centimeters'), (73, 'Square Foot/Square Feet'), (74, 'Square Inch/Square Inches'), (12, 'Square Meter/Square Meters'), (75, 'Square Mile/Square Miles'), (76, 'Square Yard/Square Yards'), (77, 'Stone/Stones'), (84, 'Strand/Strands'), (11, 'Ton/Tons'), (78, 'Tonne/Tonnes'), (79, 'Tray/Trays'), (83, 'Twenty-Foot Container'), (25, 'Unit/Units'), (80, 'Volt/Volts'), (81, 'Watt/Watts'), (82, 'Wp'), (23, 'Yard/Yards')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='supplyability',
            name='supply_unit',
            field=models.IntegerField(default=20, verbose_name='产量单位', choices=[(26, 'Acre/Acres'), (27, 'Ampere/Amperes'), (1, 'Bag/Bags'), (19, 'Barrel/Barrels'), (91, 'Blade/Blades'), (28, 'Box/Boxes'), (18, 'Bushel/Bushels'), (90, 'Carat/Carats'), (29, 'Carton/Cartons'), (30, 'Case/Cases'), (31, 'Centimeter/Centimeters'), (32, 'Chain/Chains'), (92, 'Combo/Combos'), (33, 'Cubic Centimeter/Cubic Centimeters'), (34, 'Cubic Foot/Cubic Feet'), (35, 'Cubic Inch/Cubic Inches'), (13, 'Cubic Meter/Cubic Meters'), (36, 'Cubic Yard/Cubic Yards'), (37, 'Degrees Celsius'), (38, 'Degrees Fahrenheit'), (14, 'Dozen/Dozens'), (39, 'Dram/Drams'), (40, 'Fluid Ounce/Fluid Ounces'), (41, 'Foot/Feet'), (88, 'Forty-Foot Container'), (42, 'Furlong/Furlongs'), (15, 'Gallon/Gallons'), (43, 'Gill/Gills'), (44, 'Grain/Grains'), (17, 'Gram/Grams'), (87, 'Gross'), (45, 'Hectare/Hectares'), (46, 'Hertz'), (47, 'Inch/Inches'), (48, 'Kiloampere/Kiloamperes'), (16, 'Kilogram/Kilograms'), (49, 'Kilohertz'), (10, 'Kilometer/Kilometers'), (50, 'Kiloohm/Kiloohms'), (51, 'Kilovolt/Kilovolts'), (52, 'Kilowatt/Kilowatts'), (22, 'Liter/Liters'), (9, 'Long Ton/Long Tons'), (53, 'Megahertz'), (8, 'Meter/Meters'), (7, 'Metric Ton/Metric Tons'), (54, 'Mile/Miles'), (55, 'Milliampere/Milliamperes'), (24, 'Milligram/Milligrams'), (56, 'Millihertz'), (57, 'Milliliter/Milliliters'), (58, 'Millimeter/Millimeters'), (59, 'Milliohm/Milliohms'), (60, 'Millivolt/Millivolts'), (61, 'Milliwatt/Milliwatts'), (62, 'Nautical Mile/Nautical Miles'), (63, 'Ohm/Ohms'), (6, 'Ounce/Ounces'), (21, 'Pack/Packs'), (5, 'Pair/Pairs'), (86, 'Pallet/Pallets'), (64, 'Parcel/Parcels'), (65, 'Perch/Perches'), (4, 'Piece/Pieces'), (66, 'Pint/Pints'), (85, 'Plant/Plants'), (67, 'Pole/Poles'), (3, 'Pound/Pounds'), (68, 'Quart/Quarts'), (69, 'Quarter/Quarters'), (70, 'Rod/Rods'), (71, 'Roll/Rolls'), (20, 'Set/Sets'), (89, 'Sheet/Sheets'), (2, 'Short Ton/Short Tons'), (72, 'Square Centimeter/Square Centimeters'), (73, 'Square Foot/Square Feet'), (74, 'Square Inch/Square Inches'), (12, 'Square Meter/Square Meters'), (75, 'Square Mile/Square Miles'), (76, 'Square Yard/Square Yards'), (77, 'Stone/Stones'), (84, 'Strand/Strands'), (11, 'Ton/Tons'), (78, 'Tonne/Tonnes'), (79, 'Tray/Trays'), (83, 'Twenty-Foot Container'), (25, 'Unit/Units'), (80, 'Volt/Volts'), (81, 'Watt/Watts'), (82, 'Wp'), (23, 'Yard/Yards')]),
            preserve_default=True,
        ),
    ]

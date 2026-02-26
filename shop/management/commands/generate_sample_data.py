from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Product, Order, OrderItem, Report
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Generate sample products and reports for testing"

    def handle(self, *args, **options):
        self.stdout.write("Generating sample data...")

        # Create sample products (20 items per category)
        self.create_products()

        # Create 5 reports with data
        self.create_reports()

        self.stdout.write(self.style.SUCCESS("Successfully generated sample data!"))

    def create_products(self):
        women_clothing = [
            ("Floral Summer Dress", 2500, "Floral Summer Dress.jpg"),
            ("Elegant Maxi Dress", 4500, "ElegantMaxiDress.jpg"),
            ("Casual A-Line Skirt", 1800, "CasualA-LineSkirt.jpg"),
            ("Silk Blouse", 3200, "SilkBlouse.jpg"),
            ("Denim Jacket", 4000, "DenimJacket.jpg"),
            ("Cotton T-Shirt", 1200, "CottonT-Shirt.jpg"),
            ("Linen Pants", 2800, "LinenPants.jpg"),
            ("Pencil Skirt", 2200, "PencilSkirt.jpg"),
            ("Wrap Dress", 3500, "WrapDress.jpg"),
            ("Cardigan Sweater", 3000, "CardiganSweater.jpg"),
            ("Cargo Pants", 2600, "CargoPants.jpg"),
            ("Printed Top", 1500, "PrintedTop.jpg"),
            ("Midi Skirt", 2000, "MidiSkirt.jpg"),
            ("Knit Sweater", 3500, "KnitSweater.jpg"),
            ("Wide Leg Pants", 2400, "WideLegPants.jpg"),
            ("Off-Shoulder Top", 1800, "Off-ShoulderTop.jpg"),
            ("Palazzo Pants", 2200, "PalazzoPants.jpg"),
            ("Turtleneck", 2000, "Turtleneck.jpg"),
            ("Blazer", 5000, "Blazer.jpg"),
            ("Cropped Jacket", 4500, "CroppedJacket.jpg"),
        ]

        women_shoes = [
            ("High Heel Pumps", 4500, "High Heel Pumps.jpg"),
            ("Flat Sandals", 1800, "FlatSandals.jpg"),
            ("Ankle Boots", 5500, "AnkleBoots.jpg"),
            ("Sneakers", 4000, "Sneakers.jpg"),
            ("Wedges", 3200, "Wedges.jpg"),
            ("Loafers", 2800, "Loafers.jpg"),
            ("Ballet Flats", 2000, "BalletFlats.jpg"),
            ("Strappy Heels", 3800, "StrappyHeels.jpg"),
            ("Espadrilles", 2200, "Espadrilles.jpg"),
            ("Mules", 2500, "Mules.jpg"),
            ("Platform Heels", 4200, "PlatformHeels.jpg"),
            ("Knee High Boots", 7000, "KneeHighBoots.jpg"),
            ("Slip Ons", 1800, "SlipOns.jpg"),
            ("Block Heels", 3500, "BlockHeels.jpg"),
            ("Running Shoes", 5000, "RunningShoes.jpg"),
            ("Slides", 1500, "Slides.jpg"),
            ("Chelsea Boots", 6000, "ChelseaBoots.jpg"),
            ("Stiletto Heels", 4800, "StilettoHeels.jpg"),
            ("Comfort Flats", 2000, "ComfortFlats.jpg"),
            ("Jelly Sandals", 1200, "JellySandals.jpg"),
        ]

        women_handbags = [
            ("Leather Tote Bag", 6500, "LeatherToteBag.jpg"),
            ("Crossbody Bag", 3500, "CrossbodyBag.jpg"),
            ("Clutch Purse", 2000, "ClutchPurse.jpg"),
            ("Backpack", 4500, "Backpack.jpg"),
            ("Shoulder Bag", 4000, "ShoulderBag.jpg"),
            ("Satchel", 5500, "Satchel.jpg"),
            ("Bucket Bag", 3800, "BucketBag.jpg"),
            ("Mini Bag", 2500, "MiniBag.jpg"),
            ("Hobo Bag", 4200, "HoboBag.jpg"),
            ("Wristlet", 1500, "Wristlet.jpg"),
            ("Messenger Bag", 3800, "MessengerBag.jpg"),
            ("Tote Bag", 5000, "ToteBag.jpg"),
            ("Evening Bag", 2800, "EveningBag.jpg"),
            ("Weekend Bag", 6000, "WeekendBag.jpg"),
            ("Saddle Bag", 3200, "SaddleBag.jpg"),
            ("Drawstring Bag", 2200, "DrawstringBag.jpg"),
            ("Envelope Clutch", 2500, "EnvelopeClutch.jpg"),
            ("Fanny Pack", 1800, "FannyPack.jpg"),
            ("Shopping Bag", 3500, "ShoppingBag.jpg"),
            ("Phone Purse", 1500, "PhonePurse.jpg"),
        ]

        men_clothing = [
            ("Slim Fit Shirt", 2500, "SlimFitShirt.jpg"),
            ("Chino Pants", 3000, "ChinoPants.jpg"),
            ("Denim Jeans", 3500, "DenimJeans.jpg"),
            ("Polo Shirt", 1800, "PoloShirt.jpg"),
            ("Casual Blazer", 5500, "CasualBlazer.jpg"),
            ("Cotton T-Shirt", 1200, "CottonT-Shirt.jpg"),
            ("Linen Shirt", 2200, "LinenShirt.jpg"),
            ("Cargo Shorts", 2000, "CargoShorts.jpg"),
            ("V-Neck Sweater", 2800, "V-NeckSweater.jpg"),
            ("Hoodie", 3000, "Hoodie.jpg"),
            ("Dress Pants", 3200, "DressPants.jpg"),
            ("Casual Jacket", 4500, "CasualJacket.jpg"),
            ("Oxford Shirt", 2800, "OxfordShirt.jpg"),
            ("Track Pants", 2200, "TrackPants.jpg"),
            ("Cardigan", 2500, "Cardigan.jpg"),
            ("Flannel Shirt", 2400, "FlannelShirt.jpg"),
            ("Slim Fit Jeans", 3800, "SlimFitJeans.jpg"),
            ("Wool Coat", 8000, "WoolCoat.jpg"),
            ("Bomber Jacket", 5000, "BomberJacket.jpg"),
            ("Knit Polo", 2600, "KnitPolo.jpg"),
        ]

        men_shoes = [
            ("Leather Oxford", 6000, "LeatherOxford.jpg"),
            ("Casual Loafers", 4000, "CasualLoafers.jpg"),
            ("Canvas Sneakers", 3000, "CanvasSneakers.jpg"),
            ("Boat Shoes", 3500, "BoatShoes.jpg"),
            ("Dress Boots", 7000, "DressBoots.jpg"),
            ("Running Shoes", 5000, "RunningShoes.jpg"),
            ("Chelsea Boots", 6500, "ChelseaBoots.jpg"),
            ("Sandals", 1500, "Sandals.jpg"),
            ("Brogues", 5500, "Brogues.jpg"),
            ("Slip Ons", 2500, "SlipOns.jpg"),
            ("Derby Shoes", 5000, "DerbyShoes.jpg"),
            ("Athletic Shoes", 4500, "AthleticShoes.jpg"),
            ("Moccasins", 3200, "Moccasins.jpg"),
            ("Trainers", 3800, "Trainers.jpg"),
            ("Work Boots", 6000, "WorkBoots.jpg"),
            ("Espadrilles", 2000, "Espadrilles.jpg"),
            ("Monk Strap", 5800, "MonkStrap.jpg"),
            ("Slippers", 1800, "Slippers.jpg"),
            ("Hiking Boots", 7000, "HikingBoots.jpg"),
            ("Golf Shoes", 4500, "GolfShoes.jpg"),
        ]

        men_watches = [
            ("Classic Leather Watch", 8000, "ClassicLeatherWatch.jpg"),
            ("Stainless Steel Watch", 12000, "StainlessSteelWatch.jpg"),
            ("Chronograph Watch", 15000, "ChronographWatch.jpg"),
            ("Smart Watch", 18000, "SmartWatch.jpg"),
            ("Diving Watch", 10000, "DivingWatch.jpg"),
            ("Minimalist Watch", 6000, "MinimalistWatch.jpg"),
            ("Automatic Watch", 20000, "AutomaticWatch.jpg"),
            ("Digital Watch", 4000, "DigitalWatch.jpg"),
            ("Sport Watch", 7000, "SportWatch.jpg"),
            ("Gold Plated Watch", 25000, "GoldPlatedWatch.jpg"),
            ("Titanium Watch", 16000, "TitaniumWatch.jpg"),
            ("Skeleton Watch", 22000, "SkeletonWatch.jpg"),
            ("Pilot Watch", 14000, "PilotWatch.jpg"),
            ("Field Watch", 5000, "FieldWatch.jpg"),
            ("Dress Watch", 9000, "DressWatch.jpg"),
            ("Racing Watch", 13000, "RacingWatch.jpg"),
            ("Aviator Watch", 11000, "AviatorWatch.jpg"),
            ("Luxury Watch", 35000, "LuxuryWatch.jpg"),
            ("Casual Watch", 3500, "CasualWatch.jpg"),
            ("Hybrid Smart Watch", 14000, "HybridSmartWatch.jpg"),
        ]

        products_data = [
            (women_clothing, "women", "clothing"),
            (women_shoes, "women", "shoes"),
            (women_handbags, "women", "handbags"),
            (men_clothing, "men", "clothing"),
            (men_shoes, "men", "shoes"),
            (men_watches, "men", "watches"),
        ]

        for items, category, subcategory in products_data:
            for name, price, image_name in items:
                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": f"High quality {name.lower()} for {category}",
                        "price": price,
                        "category": category,
                        "subcategory": subcategory,
                        "stock": random.randint(10, 100),
                        "image": f"products/{image_name}",
                    },
                )
                if not created:
                    product.image = f"products/{image_name}"
                    product.price = price
                    product.category = category
                    product.subcategory = subcategory
                    product.save()

        self.stdout.write(f"Created/verified {Product.objects.count()} products")

    def create_reports(self):
        # Report 1: Sales Report
        paid_orders = Order.objects.filter(status="PAID")
        sales_data = {
            "total_orders": paid_orders.count(),
            "total_revenue": sum(o.get_grand_total() for o in paid_orders),
            "items": [
                {
                    "order": o.tracking_number,
                    "amount": o.get_grand_total(),
                    "date": str(o.created_at.date()),
                }
                for o in paid_orders[:20]
            ],
        }
        Report.objects.get_or_create(
            report_type="sales",
            title="Monthly Sales Report",
            defaults={"data": sales_data},
        )

        # Report 2: Inventory Report
        products = Product.objects.all()[:20]
        inventory_data = {
            "total_products": Product.objects.count(),
            "low_stock": Product.objects.filter(stock__lt=10).count(),
            "items": [
                {
                    "name": p.name,
                    "category": p.category,
                    "stock": p.stock,
                    "price": p.price,
                }
                for p in products
            ],
        }
        Report.objects.get_or_create(
            report_type="inventory",
            title="Current Inventory Report",
            defaults={"data": inventory_data},
        )

        # Report 3: Orders Report
        orders = Order.objects.all()[:20]
        orders_data = {
            "total_orders": Order.objects.count(),
            "pending": Order.objects.filter(status="PENDING").count(),
            "paid": Order.objects.filter(status="PAID").count(),
            "items": [
                {
                    "tracking": o.tracking_number,
                    "buyer": o.buyer.username,
                    "status": o.status,
                    "total": o.get_grand_total(),
                }
                for o in orders
            ],
        }
        Report.objects.get_or_create(
            report_type="orders",
            title="Orders Summary Report",
            defaults={"data": orders_data},
        )

        # Report 4: Customer Report
        customers = User.objects.filter(orders__isnull=False).distinct()[:20]
        customers_data = {
            "total_customers": User.objects.count(),
            "customers_with_orders": customers.count(),
            "items": [
                {"username": u.username, "email": u.email, "orders": u.orders.count()}
                for u in customers
            ],
        }
        Report.objects.get_or_create(
            report_type="customers",
            title="Customer Analysis Report",
            defaults={"data": customers_data},
        )

        # Report 5: Product Performance Report
        top_products = Product.objects.all()[:20]
        product_data = {
            "items": [
                {
                    "name": p.name,
                    "category": p.category,
                    "price": p.price,
                    "stock": p.stock,
                }
                for p in top_products
            ]
        }
        Report.objects.get_or_create(
            report_type="products",
            title="Product Performance Report",
            defaults={"data": product_data},
        )

        self.stdout.write(f"Created/verified {Report.objects.count()} reports")

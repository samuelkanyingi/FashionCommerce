from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = "Fix product categories based on product names"

    def handle(self, *args, **options):
        # Women shoes and items that should be women
        women_shoes = [
            "Espadrilles",
            "Slip Ons",
            "Running Shoes",
            "Chelsea Boots",
            "Ankle Boots",
            "Ballet Flats",
            "Heels",
            "Stiletto",
            "Wedges",
            "Loafers",
            "Moccasins",
            "Sandals",
            "Slides",
            "Mules",
            "High Heel",
            "Platform",
            "Strappy",
            "Sneakers",
            "Athletic",
        ]

        # Women clothing
        women_clothing = [
            "Floral",
            "Maxi",
            "Skirt",
            "Blouse",
            "Jacket",
            "T-Shirt",
            "Linen Pants",
            "Pencil",
            "Wrap Dress",
            "Cardigan",
            "Cargo Pants",
            "Printed Top",
            "Midi",
            "Knit Sweater",
            "Wide Leg",
            "Off-Shoulder",
            "Palazzo",
            "Turtleneck",
            "Cropped",
            "Blazer",
            "Silk",
            "Denim",
        ]

        # Women handbags
        women_handbags = [
            "Bag",
            "Clutch",
            "Purse",
            "Tote",
            "Satchel",
            "Crossbody",
            "Bucket",
            "Hobo",
            "Messenger",
            "Evening",
            "Wristlet",
            "Fanny",
            "Shoulder",
            "Mini",
            "Wallet",
            "Backpack",
        ]

        # Men watches
        men_watches = [
            "Watch",
            "Chronograph",
            "Pilot",
            "Diving",
            "Field",
            "Racing",
            "Skeleton",
            "Smart",
            "Sport",
            "Classic",
            "Luxury",
            "Titanium",
            "Stainless",
            "Aviator",
            "Gold Plated",
        ]

        # Men shoes
        men_shoes = [
            "Boat",
            "Brogues",
            "Derby",
            "Oxford",
            "Monk Strap",
            "Work Boots",
            "Dress Boots",
            "Hiking",
            "Golf",
            "Trainers",
        ]

        fixed_count = 0

        for product in Product.objects.all():
            old_category = product.category
            old_subcategory = product.subcategory

            # Check for women items
            if any(word.lower() in product.name.lower() for word in women_handbags):
                product.category = "women"
                product.subcategory = "handbags"
            elif any(word.lower() in product.name.lower() for word in women_shoes):
                product.category = "women"
                product.subcategory = "shoes"
            elif any(word.lower() in product.name.lower() for word in women_clothing):
                product.category = "women"
                product.subcategory = "clothing"

            # Check for men watches
            elif any(word.lower() in product.name.lower() for word in men_watches):
                product.category = "men"
                product.subcategory = "watches"

            # Check for men shoes
            elif any(word.lower() in product.name.lower() for word in men_shoes):
                product.category = "men"
                product.subcategory = "shoes"

            if (
                product.category != old_category
                or product.subcategory != old_subcategory
            ):
                self.stdout.write(
                    f"Fixed: {product.name} ({old_category}/{old_subcategory}) -> ({product.category}/{product.subcategory})"
                )
                product.save()
                fixed_count += 1

        self.stdout.write(self.style.SUCCESS(f"\nFixed {fixed_count} products!"))

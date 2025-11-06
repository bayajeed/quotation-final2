from .models import QuotationGroup, QuotationItem, Item, ItemGroup, Unit

def number_to_words_indian(num):
    if num == 0:
        return 'Zero'

    num = int(num) # Ensure we are working with an integer

    ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
            'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
            'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

    def two_digits(n):
        if n < 20:
            return ones[n]
        return tens[n // 10] + (' ' + ones[n % 10] if n % 10 != 0 else '')

    def three_digits(n):
        if n < 100:
            return two_digits(n)
        return ones[n // 100] + ' hundred' + (' and ' + two_digits(n % 100) if n % 100 != 0 else '')

    output = ''
    crore = num // 10000000
    num %= 10000000
    lakh = num // 100000
    num %= 100000
    thousand = num // 1000
    num %= 1000

    if crore > 0:
        output += three_digits(crore) + ' crore '
    if lakh > 0:
        output += three_digits(lakh) + ' lac '
    if thousand > 0:
        output += three_digits(thousand) + ' thousand '
    if num > 0:
        output += three_digits(num)

    return output.strip().replace('  ', ' ').title()

def process_groups(request, quotation):
    groups_data = {}
    for key, value in request.POST.items():
        if not key.startswith('groups-'):
            continue

        parts = key.split('-')
        try:
            if len(parts) < 3:
                continue

            group_index = int(parts[1])
            field_type = parts[2]

            if group_index not in groups_data:
                groups_data[group_index] = {'items': {}}

            if field_type == 'name' and len(parts) == 3:
                groups_data[group_index]['name'] = value
            elif field_type == 'items' and len(parts) == 5:
                item_index = int(parts[3])
                item_field = parts[4]
                if item_index not in groups_data[group_index]['items']:
                    groups_data[group_index]['items'][item_index] = {}
                groups_data[group_index]['items'][item_index][item_field] = value
        except (ValueError, IndexError):
            # Safely ignore any key that doesn't match the expected pattern
            continue

    # Clear existing groups to rebuild them
    quotation.groups.all().delete()
    
    for index, data in sorted(groups_data.items()):
        group_name = data.get('name', '').strip()
        if not group_name:
            continue # Don't create a group without a name

        group = QuotationGroup.objects.create(quotation=quotation, name=group_name)

        for item_index, item_data in sorted(data.get('items', {}).items()):
            description = item_data.get('description', '').strip()
            if not description:
                continue # Skip empty item rows

            try:
                qty = float(item_data.get('qty') or '1')
            except ValueError:
                qty = 1.0

            try:
                unit_price = float(item_data.get('unit_price') or '0')
            except ValueError:
                unit_price = 0.0

            unit_name = item_data.get('unit', '').strip()
            unit = None
            if unit_name:
                unit, _ = Unit.objects.get_or_create(name=unit_name)

            item_id = item_data.get('item_id')
            item = None
            if item_id:
                try:
                    item = Item.objects.get(id=item_id)
                except Item.DoesNotExist:
                    pass # Item not found, will be treated as a custom item

            # If no item is found, create a QuotationItem with a description only.
            if not item:
                QuotationItem.objects.create(
                    group=group,
                    description=description,
                    qty=qty,
                    unit_price=unit_price,
                    unit=unit
                )
            else:
                QuotationItem.objects.create(
                    group=group,
                    item=item,
                    qty=qty,
                    unit_price=unit_price,
                    unit=unit
                )

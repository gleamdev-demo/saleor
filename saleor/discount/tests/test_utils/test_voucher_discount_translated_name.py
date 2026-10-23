import pytest

from ....order import OrderStatus
from ... import DiscountType, VoucherType
from ...models import OrderDiscount, OrderLineDiscount, VoucherTranslation
from ...utils.voucher import create_or_update_voucher_discount_objects_for_order


@pytest.mark.parametrize(
    ("_case", "translation_language_code", "translation_name", "expected_name"),
    [
        ("translation in order language", "fr", "Bon de réduction", "Bon de réduction"),
        ("translation in other language", "de", "Gutschein", ""),
        ("translation without name", "fr", None, ""),
    ],
)
def test_order_level_voucher_discount_translated_name(
    _case,
    translation_language_code,
    translation_name,
    expected_name,
    order_with_lines,
    voucher,
):
    # given
    assert voucher.type == VoucherType.ENTIRE_ORDER

    order = order_with_lines
    order.status = OrderStatus.UNCONFIRMED
    order.language_code = "fr"
    order.voucher = voucher
    order.voucher_code = voucher.codes.first().code

    VoucherTranslation.objects.create(
        voucher=voucher,
        language_code=translation_language_code,
        name=translation_name,
    )

    # when
    create_or_update_voucher_discount_objects_for_order(order)

    # then
    discount = OrderDiscount.objects.get(order=order, type=DiscountType.VOUCHER)
    assert discount.translated_name == expected_name


def test_order_level_voucher_discount_translated_name_updated(
    order_with_lines, voucher
):
    # given
    order = order_with_lines
    order.status = OrderStatus.UNCONFIRMED
    order.language_code = "fr"
    order.voucher = voucher
    order.voucher_code = voucher.codes.first().code

    create_or_update_voucher_discount_objects_for_order(order)
    discount = OrderDiscount.objects.get(order=order, type=DiscountType.VOUCHER)
    assert discount.translated_name == ""

    translated_name = "Bon de réduction"
    VoucherTranslation.objects.create(
        voucher=voucher, language_code=order.language_code, name=translated_name
    )

    # when
    create_or_update_voucher_discount_objects_for_order(order)

    # then
    discount.refresh_from_db(fields=("translated_name",))
    assert discount.translated_name == translated_name


@pytest.mark.parametrize(
    ("_case", "translation_language_code", "expected_name"),
    [
        ("translation in order language", "fr", "Bon produit"),
        ("translation in other language", "de", ""),
    ],
)
def test_line_level_voucher_discount_translated_name(
    _case,
    translation_language_code,
    expected_name,
    order_with_lines,
    voucher_specific_product_type,
):
    # given
    voucher = voucher_specific_product_type
    order = order_with_lines
    order.status = OrderStatus.UNCONFIRMED
    order.language_code = "fr"

    discounted_line = order.lines.first()
    voucher.variants.add(discounted_line.variant)
    order.voucher = voucher
    order.voucher_code = voucher.codes.first().code

    VoucherTranslation.objects.create(
        voucher=voucher, language_code=translation_language_code, name="Bon produit"
    )

    # when
    create_or_update_voucher_discount_objects_for_order(order)

    # then
    discount = OrderLineDiscount.objects.get(
        line=discounted_line, type=DiscountType.VOUCHER
    )
    assert discount.translated_name == expected_name


def test_line_level_voucher_discount_translated_name_updated(
    order_with_lines, voucher_specific_product_type
):
    # given
    voucher = voucher_specific_product_type
    order = order_with_lines
    order.status = OrderStatus.UNCONFIRMED
    order.language_code = "fr"

    discounted_line = order.lines.first()
    voucher.variants.add(discounted_line.variant)
    order.voucher = voucher
    order.voucher_code = voucher.codes.first().code

    create_or_update_voucher_discount_objects_for_order(order)
    discount = OrderLineDiscount.objects.get(
        line=discounted_line, type=DiscountType.VOUCHER
    )
    assert discount.translated_name == ""

    translated_name = "Bon produit"
    VoucherTranslation.objects.create(
        voucher=voucher, language_code=order.language_code, name=translated_name
    )

    # when
    create_or_update_voucher_discount_objects_for_order(order)

    # then
    discount.refresh_from_db(fields=("translated_name",))
    assert discount.translated_name == translated_name

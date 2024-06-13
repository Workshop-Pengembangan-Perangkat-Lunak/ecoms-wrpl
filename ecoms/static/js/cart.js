(function ($) {
  "use strict";

  $(document).ready(function () {
    // Calculate and display item totals and subtotal when page loads
    updateItemTotals();
    updateSubtotal();
  });

  // Product Quantity
  $(".quantity button").on("click", function () {
    var button = $(this);
    var oldValue = button.parent().parent().find("input").val();
    if (button.hasClass("btn-plus")) {
      var newVal = parseFloat(oldValue) + 1;
    } else {
      if (oldValue > 0) {
        var newVal = parseFloat(oldValue) - 1;
      } else {
        newVal = 0;
      }
    }
    button.parent().parent().find("input").val(newVal);

    var item = $(this).closest(".cart-item");
    updateItemTotal(item);
    updateSubtotal();
  });

  $(".remove-cart").click(function () {
    var item = $(this).closest(".cart-item");
    item.remove();
    updateSubtotal();
  });

  function updateItemTotals() {
    $(".cart-item").each(function () {
      updateItemTotal($(this));
    });
  }

  function updateItemTotal(item) {
    var pricePerItem = parseFloat(item.find(".item-price").text());
    var quantity = parseInt(item.find(".item-quantity").val());
    var total = pricePerItem * quantity;
    item.find(".item-total").text(total);
  }

  function updateSubtotal() {
    var subtotal = 0;
    $(".item-total").each(function () {
      subtotal += parseFloat($(this).text());
    });
    $(".subtotal").text(subtotal);
  }
})(jQuery);

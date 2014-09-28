jQuery(function ($) {

    var $fieldset = $("fieldset"),
        $form = $("form", $fieldset);

    $form.validate({
         submitHandler: function (thisForm) {
            thisForm.submit();
            $fieldset.attr("disabled", "disabled");
        }
    });
});

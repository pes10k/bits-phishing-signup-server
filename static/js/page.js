jQuery(function ($) {

    var $fieldset = $("fieldset"),
        $form = $("form", $fieldset);

    $form.validate({
         submitHandler: function (thisForm) {
            // some other code
            // maybe disabling submit button
            // then:
            $fieldset.attr("disabled", "disabled");
            // thisForm.submit();
        }
    });
});

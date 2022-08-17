// passing data on to the form
$('#ModifySuggestionModal').on('show.bs.modal', function (event) {
    let date = $(event.relatedTarget).data('date')
    $(this).find('.modal-body #date').val(date)
    $.ajax({
        type: 'POST',
        url: '{{ url_for('.get_choices') }}',
        data: {'date': date}
      }).then(function (data) {
        // re-init select2
        $('.suggestion-select2').html('').select2(
            {
                dropdownAutoWidth : true,
                width : '100%',
                dropdownParent: $('#ModifySuggestionModal')
            }
        );
        choices = data.choices
        console.log(choices);
        for (var key in choices) {
            var newOption = new Option(choices[key], key, false, false);
            $('.suggestion-select2').append(newOption).trigger('change');
        }
        $('.suggestion-select2').val(data.suggestion).trigger('change');
        console.log($('.suggestion-select2'))
      })

})
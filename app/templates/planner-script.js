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
        choices = Object.entries(data.filtered).map(([k,v]) => {
            return {id: k, text: v}
        })
        others = Object.entries(data.other).map(([k,v]) => {
            return {id: k, text: v}
        })
        console.log(choices)
        $('.suggestion-select2').html('').select2(
            {
                dropdownAutoWidth : true,
                width : '100%',
                dropdownParent: $('#ModifySuggestionModal'),
                data: [{
                        text: "Filtered",
                        children: choices
                    },
                    {
                        text: "All",
                        children: others
                }]
            }
        );
        $('.suggestion-select2').val(data.suggestion).trigger('change');
      })

})
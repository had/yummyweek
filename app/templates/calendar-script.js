// enabling select2
$(document).ready(function() {
    $('.meals-select2').select2(
        {
            dropdownAutoWidth : true,
            width : '100%',
            dropdownParent: $('#AddMealModal')
        }
    );
});

// passing data on to the form
$('#AddMealModal').on('show.bs.modal', function (event) {
    let day = $(event.relatedTarget).data('day')
    $(this).find('.modal-body #day').val(day)
    $.ajax({
        type: 'POST',
        url: '{{ url_for('.selected_meals', year=year, month=month) }}',
        data: {'day': day}
      }).then(function (data) {
        $('.meals-select2').val(data);
        $('.meals-select2').trigger('change');
      })
      $.ajax({
        type: 'POST',
        url: '{{ url_for('.suggested_meals', year=year, month=month) }}',
        data: {'day': day}
      }).then(function (data) {
        $('#suggestions').empty();
        if (jQuery.isEmptyObject(data)) {
            $('#sugg-panel').hide()
        } else {
            $('#sugg-panel').show()
            // Create list of suggestions
            $.each(data, function(key, name) {
                $('#suggestions').append(
                    '<li class="list-group-item" data-id="' + key + '">' + name + '</li>');
            })
            // Attach to the "use" button a handler to re-read the list and append it to select2
            $('#use_sugg').click(function() {
                $(document).find('.modal-body #remove_suggestions').val('yes')
                var sugg = []
                $('#suggestions').find('li').each(function() {
                    sugg.push($(this).attr('data-id'));
                })
                $('.meals-select2').val(sugg)
                $('.meals-select2').trigger('change');
            })
        }
      })
})
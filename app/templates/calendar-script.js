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
        console.log($('.meals-select2').select2('data'))
      })
})
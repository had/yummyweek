$('#category_select2').select2(
{
    ajax: {
        url: '{{ url_for('.dish_categories') }}',
        datatype: 'json'
    },
    tags: true,
    theme: "bootstrap4"
});
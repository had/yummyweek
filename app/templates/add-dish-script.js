
{% if dish_type == "dish" %}
$('#category_select2').select2(
{% else %}
$('#elements_select2').select2(
{% endif %}
{
    ajax: {
        url: '{{ url_for('.dish_categories') }}',
        datatype: 'json'
    },
    tags: true,
    theme: "bootstrap4"
});
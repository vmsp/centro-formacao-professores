(function($, Cookies, CKEDITOR) {
'use static';

$.ajaxSetup({headers: {'X-CSRFToken': Cookies.get('csrftoken')}});

$('[data-seleccionar]').on('change', function(e) {
  var id = $(this).closest('tr').attr('data-id');
  $.ajax('/alterar_seleccionado/' + id + '/', {
     method: 'post',
     data: {seleccionada: this.checked},
   })
      .done(function(data) {
        $('#total_seleccionadas').text(data.total_seleccionadas);
      })
      .fail(function() {
        e.preventDefault();
      });
});

$('[data-sesamify-links] a').on('click', function(e) {
  e.preventDefault();
  var qs = new URLSearchParams(window.location.search);
  window.location = e.target.pathname + '?sesame=' + qs.get('sesame');
});

$('textarea').each(function() {
  CKEDITOR.replace(this, {
    contentsCss: $('link[rel=stylesheet]')
                     .map(function() {
                       return this.href;
                     })
                     .get(),
    bodyClass: 'p-2 text-hyphenate',
    extraPlugins: ['autogrow'],
    autoGrow_minHeight: 300,
    autoGrow_onStartup: true,
    toolbarGroups: [
      {name: 'styles', groups: ['styles']},
      {name: 'clipboard', groups: ['clipboard', 'undo']}, {
        name: 'editing',
        groups: ['find', 'selection', 'spellchecker', 'editing']
      },
      {name: 'links', groups: ['links']}, {name: 'insert', groups: ['insert']},
      {name: 'forms', groups: ['forms']}, {name: 'tools', groups: ['tools']},
      {name: 'document', groups: ['mode', 'document', 'doctools']},
      {name: 'basicstyles', groups: ['basicstyles', 'cleanup']},
      {name: 'others', groups: ['others']}, {
        name: 'paragraph',
        groups: ['list', 'indent', 'blocks', 'align', 'bidi', 'paragraph']
      },
      {name: 'colors', groups: ['colors']}
    ],
    removeButtons: 'Underline,Subscript,Superscript,Source,Image,Maximize'
  });
});
})(jQuery, Cookies, CKEDITOR);

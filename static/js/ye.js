$(document).ready(function(){

  backToTopButton();

  defaultFilter();

  addIdentifiers();

  initialFilterCount();

  updateFilterDisplay();

  // items grid and its settings
  var $grid = $('.grid').imagesLoaded( function() {
    // init Isotope after all images have loaded
    $grid.isotope({
      itemSelector: '.grid-item',
      percentPosition: true,
      layoutMode: 'fitRows'
    });
  });

  // filter items
  var filters = {};
  // do filtering on category button change
  $('#category-button-group').on( 'click', function( event ) {
    var checkbox = event.target;
    var $checkbox = $( checkbox );
    var group = $checkbox.parents('.button-group').attr('data-filter-group');
    // create array for filter group, if not there yet
    var filterGroup = filters[ group ];
    if ( !filterGroup ) {
      filterGroup = filters[ group ] = [];
    }
    // add/remove filter
    if ( checkbox.checked ) {
      // add filter
      filterGroup.push( checkbox.value );
    } else {
      // remove filter
      var index = filterGroup.indexOf( checkbox.value );
      filterGroup.splice( index, 1 );
    }

    var comboFilter = getComboFilter();
    $grid.isotope({ filter: comboFilter });

    checkIfItems();
    updateFilterCount();
    updateFilterDisplay();
    $('html, body').animate({ scrollTop: 0 }, 'fast');
  });
  // do filtering on color button change
  $('#color-button-group').on( 'click', function( event ) {
    var checkbox = event.target;
    var $checkbox = $( checkbox );
    var group = $checkbox.parents('.button-group').attr('data-filter-group');
    // create array for filter group, if not there yet
    var filterGroup = filters[ group ];
    if ( !filterGroup ) {
      filterGroup = filters[ group ] = [];
    }
    // add/remove filter
    if ( $(checkbox).hasClass('is-checked') ) {
      // add filter
      filterGroup.push( $(checkbox).attr('data-filter') );
    } else {
      // remove filter
      var index = filterGroup.indexOf( $(checkbox).attr('data-filter') );
      filterGroup.splice( index, 1 );
    }

    var comboFilter = getComboFilter();
    $grid.isotope({ filter: comboFilter });

    checkIfItems();
    updateFilterCount();
    updateFilterDisplay();
    $('html, body').animate({ scrollTop: 0 }, 'fast');
  });

  // change 'is-checked' class on buttons for filters
  $('#category-button-group').on( 'click', '.button', function( event ) {
    $('#category-button-group').find('.is-checked').removeClass('is-checked');
    var $button = $( event.currentTarget );
    $button.addClass('is-checked');
    // removes checked property of buttons that are not selected. acts like a set of radio buttons
    var $checkboxes = $('#category-button-group div input[type=checkbox]');
    $checkboxes.prop('checked', false)
  });

  $('#color-button-group').on( 'click', '.button', function( event ) {
    var $button = $( event.currentTarget );
    $button.toggleClass('is-checked');
  });

  function backToTopButton() {
    var btt = $('#back-to-top-btn');

    // shows button after scroll position
    $(window).scroll(function() {
      if ($('body').scrollTop() > 100 || $('html').scrollTop() > 100) {
        btt.addClass('show');
      } else {
        btt.removeClass('show');
      }
    });

    // button animation back to top
    btt.click(function() {
      $('body').animate({scrollTop: 0}, 500);
      $('html').animate({scrollTop: 0}, 500);
    });
  }

  function defaultFilter() {
    // filter for 'all' categories is selected at start
    $('#category-button-group div #all').prop('checked', true);
  }

  function addIdentifiers() {
    // add identifiers (such as title and alt text) to each item in grid based on their title
    var $items = $('.grid-item');
    $items.map(function() {
      // adds title to item so the item name is displayed when hovered on
      $(this).attr('title', $(this).children('.item-name').html().toUpperCase());
      $(this).children('img').attr('alt', $(this).children('.item-name').html().toUpperCase());
    });

    // add identifier (a title) to each category filter based on their type
    var $categoreies = $('#category-button-group div .button');
    $categoreies.map(function() {
      // adds title to category so the color name is displayed when hovered on
      $(this).attr('title', $(this).html().toUpperCase());
    });

    // add identifier (a title) to each color filter based on their color
    var $colors = $('#color-button-group .color-circle');
    $colors.map(function() {
      // adds title to color so the color name is displayed when hovered on
      $(this).attr('title', $(this).attr('id').toUpperCase());
    });
  }

  function initialFilterCount() {
    var $filterCount = $('#initial-filter-count');
    var $grid = $('.grid');
    var iso = $grid.data('isotope');
    $filterCount.text( $grid.children('.grid-item').length + ' items' );
  }

  function updateFilterCount() {
    $('#initial-filter-count').css('display', 'none')
    $('#updated-filter-count').css('display', 'block')
    var $filterCount = $('#updated-filter-count');
    var $grid = $('.grid');
    var iso = $grid.data('isotope');
    $filterCount.text( iso.filteredItems.length + ' items' );
  }

  function getComboFilter() {
    var combo = [];
    for ( var prop in filters ) {
      var group = filters[ prop ];
      if ( !group.length ) {
        // no filters in group, carry on
        continue;
      }
      // add first group
      if ( !combo.length ) {
        combo = group.slice(0);
        continue;
      }
      // add additional groups
      var nextCombo = [];
      // split group into combo: [ A, B ] & [ 1, 2 ] => [ A1, A2, B1, B2 ]
      for ( var i=0; i < combo.length; i++ ) {
        for ( var j=0; j < group.length; j++ ) {
          var item = combo[i] + group[j];
          nextCombo.push( item );
        }
      }
      combo = nextCombo;
    }
    var comboFilter = combo.join(', ');
    return comboFilter;
  }

  function updateFilterDisplay() {
    // display applied filters
    var $categoryDisplay = $('#category-filter-display');
    var $colorDisplay = $('#color-filter-display');

    var $activeCategory = $('#category-button-group div .is-checked').html().toUpperCase();

    var $activeColors = $('#color-button-group .is-checked');
    var $activeColorsList = [];
    $activeColors.map(function() {
      if ( $activeColorsList.length > 0 ) {
        $activeColorsList.push( ' + ' );
      }

      $activeColorsList.push( $(this).attr('id').toUpperCase() );
    });

    $categoryDisplay.html($activeCategory);
    $colorDisplay.html($activeColorsList);
  }

  function checkIfItems() {
    // presents text to the user, notifying them that their filter options brought back no items
    var noItemsText = $('#no-items-container');
    if ( $('.grid').css('height') == '0px' ) {
      noItemsText.css('height', 'auto');
      noItemsText.css('margin-top', '10vh');
    } else {
      noItemsText.css('height', '0');
      noItemsText.css('margin-top', '0');
    }

    updateFilterCount()
  }

});

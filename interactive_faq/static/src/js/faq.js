odoo.define('interactive_faq.faq', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.InteractiveFAQ = publicWidget.Widget.extend({
        selector: '.faq-container',
        events: {
            'input #faq-search': '_onSearch',
            'click .category-btn': '_onCategoryClick',
            'show.bs.collapse .collapse': '_onShowAnswer',
            'hide.bs.collapse .collapse': '_onHideAnswer'
        },

        start: function () {
            var def = this._super.apply(this, arguments);
            this.$('.category-btn[data-category="all"]').addClass('active');
            this._initializeTooltips();
            return def;
        },

        _initializeTooltips: function() {
            this.$('[data-toggle="tooltip"]').tooltip();
        },

        _onSearch: function (ev) {
            var searchValue = $(ev.currentTarget).val().toLowerCase();
            var hasResults = false;
            
            this.$('.faq-item').each(function() {
                var $faq = $(this);
                var question = $faq.find('.faq-question').text().toLowerCase();
                var answer = $faq.find('.card-body').text().toLowerCase();
                
                if (question.indexOf(searchValue) > -1 || answer.indexOf(searchValue) > -1) {
                    $faq.slideDown(300);
                    hasResults = true;
                } else {
                    $faq.slideUp(300);
                }
            });

            // Show/hide no results message
            if (!hasResults && searchValue.length > 0) {
                this.$('.no-results').addClass('active');
            } else {
                this.$('.no-results').removeClass('active');
            }
        },

        _onCategoryClick: function (ev) {
            ev.preventDefault();
            var $target = $(ev.currentTarget);
            var selectedCategory = $target.data('category');
            
            // Update active button with animation
            this.$('.category-btn').removeClass('active');
            $target.addClass('active');
            
            // Filter FAQ items with animation
            if (selectedCategory === 'all') {
                this.$('.faq-item').slideDown(300);
            } else {
                this.$('.faq-item').each(function() {
                    var $faq = $(this);
                    if ($faq.data('category') == selectedCategory) {
                        $faq.slideDown(300);
                    } else {
                        $faq.slideUp(300);
                    }
                });
            }
        },

        _onShowAnswer: function(ev) {
            var $item = $(ev.target).closest('.faq-item');
            $item.addClass('active');
        },

        _onHideAnswer: function(ev) {
            var $item = $(ev.target).closest('.faq-item');
            $item.removeClass('active');
        }
    });

    return publicWidget.registry.InteractiveFAQ;
});
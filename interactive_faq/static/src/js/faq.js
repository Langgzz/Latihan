odoo.define('interactive_faq.faq', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.InteractiveFAQ = publicWidget.Widget.extend({
        selector: '.faq-container',
        events: {
            'input #faq-search': '_onSearch',
            'click .category-btn': '_onCategoryClick',
        },

        start: function () {
            var def = this._super.apply(this, arguments);
            // Initial state is handled by template, but we can ensure it here
            return def;
        },

        _onSearch: function (ev) {
            var searchValue = $(ev.currentTarget).val().toLowerCase();
            var hasResults = false;
            var self = this;
            
            this.$('.faq-item').each(function() {
                var $faq = $(this);
                var question = $faq.find('.faq-question').text().toLowerCase();
                var answer = $faq.find('.card-body').text().toLowerCase();
                
                if (question.indexOf(searchValue) > -1 || answer.indexOf(searchValue) > -1) {
                    $faq.show();
                    hasResults = true;
                } else {
                    $faq.hide();
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
            
            // Update active button
            this.$('.category-btn').removeClass('active');
            $target.addClass('active');
            
            // Filter FAQ items
            if (selectedCategory === 'all') {
                this.$('.faq-item').fadeIn(200);
            } else {
                this.$('.faq-item').each(function() {
                    var $faq = $(this);
                    if ($faq.data('category') == selectedCategory) {
                        $faq.fadeIn(200);
                    } else {
                        $faq.hide();
                    }
                });
            }
        }
    });

    return publicWidget.registry.InteractiveFAQ;
});

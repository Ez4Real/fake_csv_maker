/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        '../../**/*.py',
    ],
    theme: {
        extend: {
            fontFamily: {
                helvetica: ['Helvetica Neue', 'sans-serif'],
              },
            width: {
                '650': '650px',
                '84': '84px',
                '%90': '90%',
                '%56': '56%',
                '%27': '27%',
                'p100': '100px',
                'p92': '92px',
                'p116': '116px',
                'p86': '86px',
            },
            height: {
                '445': '445px',
                '38': '38px',
                'p78': '78px'
            },
        },
        colors: {
            black: '#000000',
            gray: '#f7f7f9',
            blue: '#0275d8',
            white: '#ffffff',
            red: '#d9534f',
            fgray: '#cccccc',
            lgray: '#e5e5e5',
            green: '#5cb85c',
            vlgray: '#eceeef',
            dark: '#373a3c',
            bgray: '#999999',
        }
    },
    variants: {},
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}

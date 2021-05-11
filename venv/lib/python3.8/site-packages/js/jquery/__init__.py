from fanstatic import Library, Resource

library = Library('jquery', 'resources')

jquery = Resource(library, 'jquery-3.2.1.js', minified='jquery-3.2.1.min.js')

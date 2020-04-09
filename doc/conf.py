import shutil
import sys
import os

project = u'Ceph'
copyright = u'2016, Ceph authors and contributors. Licensed under Creative Commons Attribution Share Alike 3.0 (CC-BY-SA-3.0)'
version = 'dev'
release = 'dev'

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['**/.#*', '**/*~', 'start/quick-common.rst', '**/*.inc.rst']
if tags.has('man'):
    master_doc = 'man_index'
    exclude_patterns += ['index.rst', 'architecture.rst', 'glossary.rst', 'release*.rst',
                         'api/*',
                         'cephadm/*',
                         'cephfs/*',
                         'dev/*',
                         'governance.rst',
                         'foundation.rst',
                         'install/*',
                         'mon/*',
                         'rados/*',
                         'mgr/*',
                         'ceph-volume/*',
                         'radosgw/*',
                         'rbd/*',
                         'start/*',
                         'releases/*']
else:
    exclude_patterns += ['man_index.rst']

pygments_style = 'sphinx'

html_theme = 'ceph'
html_theme_path = ['_themes']
html_title = "Ceph Documentation"
html_logo = 'logo.png'
html_favicon = 'favicon.ico'
html_show_sphinx = False
html_static_path = ["_static"]
html_sidebars = {
    '**': ['smarttoc.html', 'searchbox.html'],
    }
html_css_files = [
    'css/custom.css',
]
sys.path.insert(0, os.path.abspath('_ext'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.graphviz',
    'sphinx.ext.todo',
    'plantweb.directive',
    'breathe',
    'edit_on_github',
    'ceph_releases',
    ]
ditaa = shutil.which("ditaa")
if ditaa is not None:
    extensions += ['sphinxcontrib.ditaa']
else:
    extensions += ['plantweb.directive']

todo_include_todos = True

top_level = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

breathe_default_project = "Ceph"
# see $(top_srcdir)/Doxyfile

breathe_build_directory = os.path.join(top_level, "build-doc")
breathe_projects = {"Ceph": os.path.join(top_level, breathe_build_directory)}
breathe_projects_source = {
    "Ceph": (os.path.join(top_level, "src/include/rados"),
             ["rados_types.h", "librados.h"])
}
breathe_domain_by_extension = {'py': 'py', 'c': 'c', 'h': 'c', 'cc': 'cxx', 'hpp': 'cxx'}

# the docs are rendered with github links pointing to master. the javascript
# snippet in _static/ceph.js rewrites the edit links when a page is loaded, to
# point to the correct branch.
edit_on_github_project = 'ceph/ceph'
edit_on_github_branch = 'master'

# handles edit-on-github and old version warning display
def setup(app):
    app.add_javascript('js/ceph.js')
    if ditaa is None:
        # add "ditaa" as an alias of "diagram"
        from plantweb.directive import DiagramDirective
        app.add_directive('ditaa', DiagramDirective)

if os.environ.get('READTHEDOCS') == 'True':
    exclude_patterns += ['**/api/*',
                         '**/api.rst']
    autodoc_mock_imports = ['ceph_module',
                            'cephfs',
                            'rados',
                            'rbd',
                            'ceph']
    pybinds = ['pybind/mgr',
               'python-common']
else:
    autodoc_mock_imports = ['ceph_module']
    pybinds = ['pybind',
               'pybind/mgr',
               'python-common']
    plantweb_defaults = {
        'engine': 'ditaa'
    }

for c in pybinds:
    pybind = os.path.join(top_level, 'src', c)
    if pybind not in sys.path:
        sys.path.insert(0, pybind)

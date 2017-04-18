from jinja2 import Template
from neo4j.v1 import GraphDatabase, basic_auth
from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "neo4j"))
session = driver.session()

def hello_world(request):
    # Get the record to render along with the template for it
    result = session.run("""
        match (r:Recipe)-[:RENDERED_WITH]->(t:Template)
        where r.name = "Cake" return r, t
    """);
    record = result.peek()
    recipe = record['r']
    template = record['t']

    # Create jinja2 template
    template_text = template.properties['template']
    jinja_template = Template(template_text)

    # Render template
    render = jinja_template.render(node=recipe)

    return Response(render)


if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

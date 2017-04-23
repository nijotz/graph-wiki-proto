from jinja2 import Template
from neo4j.v1 import GraphDatabase, basic_auth
from pyramid.config import Configurator
from pyramid.response import Response
import pyramid.httpexceptions as exc
from wsgiref.simple_server import make_server


# Connect to neo4j database and create sesssion using default username/password
driver = GraphDatabase.driver("bolt://localhost:7687",
                              auth=basic_auth("neo4j", "neo4j"))
session = driver.session()


def render_node(request):
    # Get the slug from the URL of the request
    slug = request.matchdict['slug']

    # Get the node to render along with the template for it
    result = session.run("""
        match (n)-[r:RENDERED_WITH]->(t:Template)
        where r.slug = {slug}
        return n, r, t
    """, slug=slug);
    record = result.peek()

    # If no node has that slug, 404
    if not record:
        return exc.HTTPNotFound()

    node = record['n']
    template = record['t']

    # Create jinja2 template
    template_text = template.properties['text']
    jinja_template = Template(template_text)

    # Render template
    render = jinja_template.render(node=node)

    return Response(render)


if __name__ == '__main__':
    config = Configurator()
    config.add_route('node', '/{slug}')
    config.add_view(render_node, route_name='node')

    app = config.make_wsgi_app()
    host = '0.0.0.0'
    port = 8000
    server = make_server('0.0.0.0', 8000, app)
    print("Listening on http://{host}:{port}".format(host=host, port=port))

    server.serve_forever()

// Create a recipe
create (r:Recipe {name: "Cake"})

// Create an ingredient
create (i:Ingredient {name: "Flour"})

// Link them
match (r:Recipe), (i:Ingredient)
where r.name = "Cake" and i.name = "Flour"
create (r)-[:MADE_WITH]->(i)

// Create a template to render the recipe
Create (t:Template { name: "recipe_template" })

// Link node and template
match (r:Recipe), (t:Template)
where r.name = "Cake" and t.name = "recipe_template"
create (r)-[:RENDERED_WITH]->(t)

// Set template text
match (t:Template) set t.template = "<h1>Recipe Name: {{node.properties.name}}</h1>"

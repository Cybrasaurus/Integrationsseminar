from website import create_app




app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0")

#todo rewirte landing/home page to proper one
#todo make space for all 3 DB systems
#todo grab video link from coding and in the comments in this doc
#todo overview page with all the chapters
#todo links and jumping in navbar + buttons

#todo autoconnect to cursors of the different DB-s currently only done on bootup
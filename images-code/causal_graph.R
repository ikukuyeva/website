### R 3.3

# Per http://blog.revolutionanalytics.com/2015/08/contracting-and-simplifying-a-network-graph.html
# and http://www.r-bloggers.com/an-example-of-social-network-analysis-with-r-using-package-igraph/
#
# Per http://stackoverflow.com/questions/12058556/adjusting-the-node-size-in-igraph-using-a-matrix
# adjust vertex size
library(igraph)

create_termMatrix <- function(n.row){
	set.seed(1)
	termMatrix <- matrix(round(abs(rnorm(n.row^2, mean=n.row, sd=n.row^2))),
		byrow=TRUE,
		ncol=n.row,
		nrow=n.row
		)
	index <- sample(1:(n.row^2), round(0.95*(n.row^2)), replace=FALSE)
	termMatrix[index] <- 0

	termMatrix <- as.data.frame(termMatrix)
	names(termMatrix) <- paste("Var", 1:n.row)
	row.names(termMatrix) <- paste("Var", 1:n.row)

	return(termMatrix)
}

plot_termMatrix <- function(termMatrix){
	set.seed(2)
	g <- graph.adjacency(
		as.matrix(termMatrix), 
		weighted=TRUE, 
		mode = 'directed'
		)

	# remove loops
	g <- simplify(g)
	# set labels and degrees of vertices
	V(g)$label <- V(g)$name
	V(g)$degree <- degree(g)

	# set seed to make the layout reproducible
	layout1 <- layout.fruchterman.reingold(g)
	# tkplot(g, layout=layout1)
	plot(g, layout=layout1)

	# Make it look better:
	V(g)$color <- 'goldenrod1'
	V(g)$label.cex <- 1
	V(g)$arrow.cex <- 3 * V(g)$degree / max(V(g)$degree)+ .1
	V(g)$frame.color <- NA
	egam <- (log(E(g)$weight)+.4) / max(log(E(g)$weight)+.4)
	E(g)$color <- 'darkorange3'
	E(g)$width <- egam

	tkplot(g,layout=layout1,
		vertex.label=V(g)$names,
		vertex.label.color = "black",
		vertex.size=round(runif(nrow(termMatrix), 1, 30)),
		vertex.label.family="Helvetica"
		) 
		# Font type per http://www.kateto.net/wordpress/wp-content/uploads/2015/06/Polnet%202015%20Network%20Viz%20Tutorial%20-%20Ognyanova.pdf
}


termMatrix <- create_termMatrix(25)
plot_termMatrix(termMatrix)
# Var 24 is the 'outcome variable'
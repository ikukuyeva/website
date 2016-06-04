### Per http://stats.stackexchange.com/questions/4062/how-to-plot-a-fan-polar-dendrogram-in-r
library(ape)
library(cluster) 

### Per https://rstudio-pubs-static.s3.amazonaws.com/1876_df0bf890dd54461f98719b461d987c3d.html
hc <- hclust(dist(datasets::mtcars))
hc$labels <- paste("V", 1:length(hc$labels))

set.seed(1)
op <- par(mai=rep(0.2, 4), mar=rep(0.3, 4))
	plot(as.phylo(hc), 
		type="fan",
		edge.width = runif(20, 5, 8),
		tip.color = "darkorange2",
		edge.color = "cadetblue", 
		cex=1.7
		)
par(op)


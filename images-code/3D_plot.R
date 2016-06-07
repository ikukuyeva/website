library(lattice)

corn <- read.table("corn.txt", header=TRUE, sep="\t")
summary(corn)

names(corn) <- c("Brand", "Var2", "Var1", "Container", "Outcome")
attach(corn)

# draw the surface and color codes depending on popcorn count
# wireframe(Good~Oil*Time|Brand, 

# palette = colorRampPalette(c("darkslategrey4", "white", "darkgoldenrod2"))

wireframe(Outcome~Var1*Var2|Brand, 
	auto.key=TRUE, 
	type="h", 
	cross=TRUE, 
	col.points=2, 
	type="h", 
	color.key=TRUE,  
	col =  c("grey", "transparent"), 
	drape=TRUE
	)

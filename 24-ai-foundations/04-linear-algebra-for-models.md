# Linear algebra for models

Vectors and matrices are not decoration around AI: they are the language used to represent examples, combine signals, and move information through a model.

## Why it matters

Continue from [Data, evaluation, and evidence](03-data-evaluation-and-evidence.md). Shape mistakes, unintended broadcasting, and misunderstood similarity measures can produce plausible outputs while computing the wrong function.

## How it works

A vector \(x\in\mathbb{R}^d\) stores \(d\) coordinates. The dot product \(w^Tx=\sum_iw_ix_i\) is both a weighted sum and, after normalization, a similarity score. A matrix \(W\in\mathbb{R}^{m\times d}\) maps a \(d\)-vector to an \(m\)-vector. For a batch \(X\in\mathbb{R}^{n\times d}\), \(XW^T\) computes every example's \(m\) outputs at once.

A basis chooses coordinates; changing basis can make a relationship simpler without changing the represented object. Rank counts independent directions. If features are linearly dependent, parameters may be non-identifiable even when predictions are stable. Eigenvectors identify directions preserved by a square transformation; singular value decomposition extends this idea to any matrix and orders directions by retained scale.

Norms encode geometry. The \(L_2\) norm measures Euclidean length, cosine similarity removes length, and \(L_1\) emphasizes coordinate-wise distance. These choices assert what “near” means. In an embedding system, normalization changes maximum inner-product search into cosine search; that can change rankings, not merely speed.

## Vocabulary

- **rank:** number of linearly independent directions in a matrix
- **basis:** independent vectors used as coordinates
- **singular value:** scale applied along a paired input-output direction
- **broadcasting:** implicit expansion of array dimensions during an operation

## See it yourself

Let \(x=(1,2)\), \(u=(2,4)\), and \(v=(-2,1)\). Predict the dot products before calculating. \(x^Tu=10\), while \(x^Tv=0\): \(v\) is orthogonal to \(x\), and \(u\) carries no new direction beyond \(x\). Form \(A=[x;u]\). Its determinant is zero and rank is one.

Now add \(10^{-6}v\) to \(u\). The matrix becomes full rank mathematically but remains nearly singular numerically. A solver may amplify tiny measurement errors. This demonstrates why exact shape and rank checks are insufficient evidence of a well-conditioned problem.

## Where it shows up

A recommendation service stores user and item embeddings and ranks item vectors by a dot product. If item norms grow with popularity, raw inner product combines direction with popularity. Normalizing vectors removes that magnitude signal. The decision must be evaluated against product intent; neither metric is universally correct.

## When it breaks

Silent broadcasting can compare every row with every row and explode memory. Mixed row and column conventions can transpose the intended map. Near-collinear features make coefficients unstable, and large norm differences let one feature dominate distance.

When scores change after a refactor, log tensor names, shapes, dtypes, norms, and a hand-computed row. If predictions agree but coefficients swing between fits, inspect singular values and condition number. Regularization may stabilize prediction, but it does not recover a uniquely identifiable explanation.

## Practice

**Observe:** calculate a two-by-two matrix-vector product by hand and match NumPy output exactly. **Build:** implement cosine and dot-product ranking over five vectors; completion means a test shows where their rankings differ. **Break:** duplicate one feature with tiny noise, fit least squares repeatedly, and capture unstable coefficients with stable predictions.

**Say it out loud:** explain why a high-dimensional vector is a representation, not the real-world object.

## Check yourself

1. Why can two parameter vectors make nearly identical predictions?
2. What does normalization discard, and when might that be harmful?
3. Which evidence distinguishes a shape bug from an ill-conditioned matrix?
4. Why does rank one imply that a second row adds no independent direction?

## Sources

### REQUIRED

- [The Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/)

### RECOMMENDED

- [NumPy linear algebra documentation](https://numpy.org/doc/stable/reference/routines.linalg.html)

### DEEP DIVE

- [MIT 18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)

## Next

Continue to [Calculus and gradient reasoning](05-calculus-and-gradient-reasoning.md).

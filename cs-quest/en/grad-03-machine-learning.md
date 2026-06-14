# 🔭 GRAD 3: The Observatory of Intelligence — Machine Learning and AI

> At the highest tower of the Heavens stands an observatory that gazes beyond the stars.
> The astronomer says: "Here we **do not write rules.**
> We **let the data speak and let the machine learn the patterns.**
> But —— use it without knowing the mathematics, and it becomes not magic but a curse.
> We ask 'why can it learn at all?' in the language of mathematics."

**Graduate-level equivalent**: Stanford **CS229 Machine Learning** / **CS231n (vision)** / **CS224n (language)** / MIT **6.036**
**Prerequisites**: World 9 (probability and linear algebra), World 6 (a feel for optimization), World 14 (algorithm design)

**What you'll learn in this chapter**
- The three categories of machine learning and their formulation
- Linear regression, logistic regression, and gradient descent
- Overfitting, generalization, and regularization (the central problem of ML)
- Neural networks and backpropagation
- Evaluation, practical pitfalls, and on to large language models

⚠️ ML stands on mathematics. Linear algebra (matrices), calculus, and probability (World 9) are the foundation.
No need to fear it —— this world aims to "grasp the core with minimal math."

---

## 📖 Lecture 1: The Three Telescopes of the Observatory — Types of Learning (20 XP)

- **Supervised learning**: learn a mapping f: x→y from pairs of input x and answer y
  - **Regression** (y is continuous: rent prediction) / **Classification** (y is discrete: spam detection)
- **Unsupervised learning**: no answers. Find structure (clustering, dimensionality reduction)
- **Reinforcement learning**: learn a policy by trial and error guided by rewards (game AI, robot control)

**The essence of machine learning**: to **do well on data you've never seen** (generalization).
Memorizing the training data is not learning. This is the central theme of everything (Lecture 3).

## 📖 Lecture 2: Predicting the Stars' Positions — Regression and Gradient Descent (20 XP)

### Linear Regression
Prediction ŷ = w·x + b. The measure of goodness is the **loss function** (mean squared error, MSE):
learning reduces to the optimization problem "**find w, b that minimize the loss.**"

### Gradient Descent — The Engine That Drives ML
On the "terrain" of the loss function, step little by little in **the direction of steepest descent (negative gradient)**:

```
w ← w − η · ∂Loss/∂w        (η is the learning rate = step size)
```

- Too big a step overshoots the valley and diverges; too small and you never arrive
- **Stochastic Gradient Descent (SGD)**: approximate the gradient with a subset (mini-batch) instead of all data → it scales to huge datasets.
  World 14's randomized mindset is here too

### Logistic Regression (classification)
Squash the output through a sigmoid into a 0–1 probability for binary classification. The loss is cross-entropy (World 9's entropy!).

## 📖 Lecture 3: The Observatory's Greatest Commandment — Overfitting and Generalization (20 XP)

This is **the single most important concept** in ML. Interviews probe whether you understand it.

- **Overfitting**: memorizing even the random noise of the training data, then missing on new data. "The honor student who crams, then fails the application problems"
- **Underfitting**: the model is too simple to even capture the training data
- **Bias-variance trade-off**: there is an optimal point between too-simple (high bias) and too-complex (high variance)

### Weapons Against Overfitting
- **Train/validation/test split**: the test data is used "exactly once" at the end. Peek at it and it's contaminated
- **Cross-validation**: split the data into k folds, use each as validation in turn, to stabilize the evaluation
- **Regularization** (L1/L2): penalize complex models and pull them back toward simplicity (the mathematical version of Occam's razor)
- **Early stopping, dropout, data augmentation**

**"Tuning repeatedly on the test data" is the worst sin.** It's peeking at answers you're not supposed to see, and it will always betray you in production.

## 📖 Lecture 4: The Deep Cosmos — Neural Networks and Backpropagation (20 XP)

A neural network stacks layers of "linear transformation + nonlinear function." Stacking layers lets it represent complex functions
(the **universal approximation theorem**: a hidden layer of sufficient width can approximate any continuous function).

### Backpropagation — The Heart of Deep Learning
Propagate the output error **backward** from output to input using the **chain rule (derivative of a composite function)** to compute each weight's gradient.
This has the same structure as World 12's compiler computation graph and World 6's recursion —— it's just **applying the chain rule recursively on a computation graph.**
Then update the weights with gradient descent (Lecture 2).

- **Activation functions**: ReLU (max(0,x)) is standard. Why is nonlinearity needed? → because stacking linear layers stays linear and adds no expressive power
- It develops into **CNNs** (vision: convolving local patterns) and **RNN/Transformer** (sequences: handling context)

## 📖 Lecture 5: Stars That Wield Language — Transformers and Large Language Models (20 XP)

The core of the modern AI star, the **Transformer**, is the **self-attention mechanism**:
it learns "how much each word in a sentence should attend to every other word," capturing context.

- **Large Language Models (LLMs)**: giant networks self-supervised to "predict the next word" on enormous text.
  Scaling up (data, parameters, compute) makes qualitatively new abilities emerge (scaling laws)
- **Transfer learning / fine-tuning**: adapt a large pre-trained model to a specific task with a small amount of data (the standard practice of modern ML)
- **Knowing the limits is also scholarship**: because an LLM probabilistically generates "plausible" words, it can state non-facts with full confidence (hallucination).
  Verification, source-checking, and human oversight are required. **Those who can articulate a tool's limits can use the tool correctly.**

> 🎓 When you want to actually embed an LLM in an app, study the API of a modern flagship model (such as Claude).
> The very Claude Code that runs this repository is one such example.

---

## ⚔️ Quests

### Quest 1: The Astronomer's Diagnosis (40 XP)

Classify each task as "regression / classification / clustering / reinforcement learning."

1. Predict tomorrow's temperature from past temperature data
2. Recognize handwritten digits as 0–9
3. Automatically group customers by purchasing behavior (no labels)
4. Learn winning moves in Go by self-play

<details>
<summary>📜 Answers</summary>

1. Regression (continuous) 2. Classification (discrete labels) 3. Clustering (unsupervised) 4. Reinforcement learning (trial and error via rewards)
</details>

### Quest 2: 💻 Implementation Quest "Turn Gradient Descent By Hand" (80 XP)

Without relying on a library's autodiff, **implement linear regression + gradient descent using only NumPy (or plain arrays)**:

- Generate data from a line y = 3x + 2 plus noise
- Compute the MSE loss and the gradients with respect to w and b, **writing the formulas yourself**
- Confirm gradient descent converges to w ≈ 3, b ≈ 2
- Multiply the learning rate by 10 and by 1/10, and **feel** the divergence and the stagnation (this is the crux of ML intuition)

### Quest 3: Autopsy of Overfitting (40 XP)

A student reports a model with "99% training accuracy, 62% test accuracy" as "high-performance."

1. Diagnose what is happening.
2. List three remedies.
3. The student then says, "I tuned hyperparameters on the test data many times and raised it to 75%." Why is this a problem?

<details>
<summary>📜 Answers</summary>

1. Overfitting. It memorized the training data's noise and does not generalize (high variance).
2. Regularization (L1/L2), adding data / data augmentation, simplifying the model, dropout, early stopping, etc.
3. It optimized against the test data, so the test no longer functions as a proxy for unseen data (information leakage). The 75% won't reproduce on real unseen data; it's an overly optimistic estimate. A separate validation set should be used.
</details>

### Quest 4: Riddles of the Deep (40 XP)

1. Without a nonlinear activation function, why does adding more layers not increase expressive power?
2. What is backpropagation doing mathematically (use the term "chain rule")?
3. Why do LLMs "confidently get things wrong"? How should you handle this in practice?

<details>
<summary>📜 Answers</summary>

1. The composition of linear transformations equals a single linear transformation, so adding layers doesn't widen the class of representable functions. Inserting nonlinearity is what enables representing complex functions.
2. It computes the gradient of the loss with respect to each weight, efficiently propagating it backward from the output layer to the input layer using the chain rule for composite functions.
3. It's trained to choose the next word by "plausibility" probabilistically, with no mechanism guaranteeing factuality. Handling: attach sources, verify against external knowledge (RAG), human review, and do not auto-finalize important decisions.
</details>

---

## 👹 Boss Battle: The Observatory's Master, "Oracle of Patterns" (200 XP)

Close your notes and fight. Win with 70% or more.

1. Distinguish supervised, unsupervised, and reinforcement learning by "what is given and what is learned."
2. Write the gradient descent update rule and describe what happens when the learning rate is too large or too small.
3. What is overfitting? Give two or more detection methods and two or more remedies.
4. Explain the bias-variance trade-off in terms of model complexity and generalization.
5. Explain that backpropagation is "applying the chain rule on a computation graph" (relate it to Worlds 6/12).
6. Why is a nonlinear activation essential in a neural network?
7. When embedding an LLM in a product, name three design considerations arising from its probabilistic nature.

<details>
<summary>📜 Answer outline</summary>

1. Supervised: learn a mapping from input–label pairs. Unsupervised: learn structure (clusters, low-dim representations) from unlabeled data. Reinforcement: learn a policy maximizing reward through interaction with an environment.
2. w ← w − η·∂Loss/∂w. Too large diverges/oscillates; too small converges extremely slowly and gets stuck in local minima more easily.
3. Memorizing training noise so performance drops on unseen data. Detection: gap between train and validation accuracy, learning curves. Remedies: regularization, more data/augmentation, simpler model, early stopping, dropout, cross-validation.
4. A simple model has high bias (can't even fit training data = underfitting); an overly complex model has high variance (overfits the training set). Generalization error is minimized at a balanced complexity.
5. To differentiate the loss with respect to each parameter, treat the network as a computation graph and recursively apply the chain rule backward from output to input to find each node's gradient efficiently. Same structure as World 12's AST evaluation and World 6's recursion.
6. Because composing linear transformations collapses to a single linear transformation and adding layers adds no expressive power; nonlinearity enables nonlinear decision boundaries and complex functions.
7. Output is probabilistic and can err (hallucination), so build fact-checking/source-verification; don't auto-finalize critical decisions that depend on nondeterministic output; defend against malicious input (prompt injection) with human oversight; continuously evaluate and monitor.
</details>

---

🏆 **Victory Reward**: Badge "🔭 Astronomer of Patterns" + 200 XP

➡️ On to the final graduate lecture: [GRAD 4: The Theory of Everything (Computer Architecture and Parallel Computing)](grad-04-architecture-parallel.md)

import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]
  for i in range(num_train):
  	scores = X[i].dot(W)
  	scores -= np.max(scores) # stabilized
  	sum_exp_scores = np.sum(np.exp(scores))
  	prob = lambda k: np.exp(scores[k]) / sum_exp_scores
  	loss += -np.log(prob(y[i]))

  	for k in range(num_classes):
  		prob_k = prob(k)
  		dW[:, k] += (prob_k - (k == y[i])) * X[i]
  loss /= num_train
  loss += .5 * reg * np.sum(W * W)
  dW /= num_train
  dW += reg*W

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = X.dot(W)
  scores -=  np.max(scores, axis=1, keepdims=True)
  sum_exp_scores = np.sum(np.exp(scores), axis=1, keepdims=True)
  probs = np.exp(scores) / sum_exp_scores
  loss = np.sum(-np.log(probs[np.arange(num_train), y]))
  loss /= num_train
  loss += .5 * reg * np.sum(W * W)
  # p_diff = probs
  # p_diff[np.arange(num_train), y] -= 1
  p_diff = np.zeros_like(probs)
  p_diff[np.arange(num_train), y] = 1
  # dW = np.dot(X.T, p_diff)
  dW = np.dot(X.T, probs-p_diff)
  dW /= num_train
  dW += reg*W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


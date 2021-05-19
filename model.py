from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

import tensorflow as tf
import tensorflow.contrib.slim as slim
import tensorflow.contrib.slim.nets as nets
from tensorflow.contrib.layers.python.layers import layers as layers_lib
from tensorflow.python.ops import variable_scope
from tensorflow.contrib.framework.python.ops import arg_scope
from tensorflow.python.framework import ops
from config import cfg
from IPython import embed

FLAGS = tf.app.flags.FLAGS

# If a model is trained using multiple GPUs, prefix all Op names with tower_name to differentiate the operations
TOWER_NAME = 'tower'

BATCHNORM_MOVING_AVERAGE_DECAY = 0.95

MOVING_AVERAGE_DECAY = 0.9999


def inference(images, num_classes, for_training=False, scope=None, reuse=None):
    """Build Inception v2 model architecture.
    Args:
      images: Images returned from inputs() or distorted_inputs().
      num_classes: number of classes
      for_training: If set to `True`, build the inference model for training.
        Kernels that operate differently for inference during training
        e.g. dropout, are appropriately configured.
      scope: optional prefix string identifying the ImageNet tower.
    Returns:
      Logits. 2-D float Tensor.
      Auxiliary Logits. 2-D float Tensor of side-head. Used for training only.
    """

    batch_norm_params = {
        'decay': BATCHNORM_MOVING_AVERAGE_DECAY,
        'epsilon': 0.001
    }

    # Set weight_decay for weights in Conv and FC layers.
    endpoints = {}

    batch_norm_params = {
        'decay': BATCHNORM_MOVING_AVERAGE_DECAY,
        'epsilon': 0.001,
        'is_training': for_training
    }

    # Set weight_decay for weights in Conv and FC layers.
    with arg_scope([slim.conv2d, slim.fully_connected],
                   weights_regularizer=slim.l2_regularizer(cfg.TRAIN.WEIGHT_DECAY),
                   weights_initializer=slim.xavier_initializer()):
        with arg_scope([slim.conv2d],
                       activation_fn=tf.nn.relu,
                       normalizer_fn=slim.batch_norm,
                       normalizer_params=batch_norm_params) as sc:
            # with slim.arg_scope(nets.inception.inception_v2_arg_scope()) as sc:
            seg_num = tf.shape(images)[1]
            images = tf.reshape(images, [-1, cfg.IMAGE_HEIGHT, cfg.IMAGE_WIDTH, cfg.TRAIN.INPUT_CHS])
            logits, _ = nets.inception.inception_v2(images, num_classes=101,
                                               is_training=for_training, dropout_keep_prob=cfg.TRAIN.DROUPOUT_RATIO, reuse=None)
            logits = tf.reshape(logits, (-1, seg_num, num_classes))
            logits = tf.reduce_mean(logits, axis=1)
            endpoints['logits'] = logits

    _activation_summaries(endpoints)

    return [endpoints['logits']]


def loss(logits, labels, batch_size=None):
    """Adds all losses for the model.
    Note the final loss is not returned. Instead, the list of losses are collected
    by slim.losses. The losses are accumulated in tower_loss() and summed to
    calculate the total loss.
    Args:
      logits: List of logits from inference(). Each entry is a 2-D float Tensor.
      labels: Labels from distorted_inputs or inputs(). 1-D tensor of shape [batch_size]
      batch_size: integer
    """

    assert batch_size is not None, 'point a value to batch_size'
    sparse_labels = tf.reshape(labels, [batch_size, 1])
    indices = tf.reshape(tf.range(batch_size), [batch_size, 1])
    concated = tf.concat(axis=1, values=[indices, sparse_labels])
    num_classes = logits[0].get_shape()[-1].value
    dense_labels = tf.sparse_to_dense(concated, [batch_size, num_classes], 1.0, 0.0)

    # Cross entropy loss for the main softmax prediction.
    slim.losses.softmax_cross_entropy(logits[0], dense_labels, label_smoothing=0, weights=1.0)


def _activation_summary(x):
    """Helper to create summaries for activations.
    Creates a summary that provides a histogram of activations.
    Creates a summary that measure the sparsity of activations.
    Args:
      x: Tensor
    """
    tensor_name = re.sub('%s_[0-9]*/' % TOWER_NAME, '', x.op.name)
    tf.summary.histogram(tensor_name + '/activations', x)
    tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(x))

def _activation_summaries(endpoints):
    with tf.name_scope('summaries'):
        for act in endpoints.values():
            _activation_summary(act)

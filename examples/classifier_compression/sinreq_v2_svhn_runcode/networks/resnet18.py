import tensorflow as tf
from .helper import *


def resnet18_noisy(input_node, netparams, err_mean, err_stddev, train_vars):
	weights_noisy, biases_noisy, err_w, err_b = helper.add_noise(netparams['weights'], netparams['biases'], err_mean, err_stddev, train_vars)
	mean, variance, scale, offset = netparams['mean'], netparams['variance'], netparams['scale'], netparams['offset']
	err_lyr = {}
	layers_err  = {}
	data_spec = helper.get_data_spec('resnet18')
	err_lyr['input'] = tf.get_variable(name='input_lyr_err', shape=(1, data_spec.crop_size, data_spec.crop_size, data_spec.channels), initializer=tf.random_normal_initializer(mean=err_mean[0], stddev=err_stddev[0]), trainable=train_vars[0])
	input_node_noisy = tf.add(input_node, err_lyr['input'])
	conv1 = conv(input_node_noisy, weights_noisy['conv1'], biases_noisy['conv1'], 2, 2, biased=False, relu=False)
	err_lyr['conv1'] = tf.get_variable(name='conv1_lyr_err', shape=conv1.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['conv1'] = tf.add(conv1, err_lyr['conv1'])
	bn_conv1 = batch_normalization(layers_err['conv1'], scale['bn_conv1'], offset['bn_conv1'], mean['bn_conv1'], variance['bn_conv1'], relu=True)
	pool1 = max_pool(bn_conv1, 3, 3, 2, 2)
	res2a_branch1 = conv(pool1, weights_noisy['res2a_branch1'], biases_noisy['res2a_branch1'], 1, 1, biased=False, relu=False)
	err_lyr['res2a_branch1'] = tf.get_variable(name='res2a_branch1_lyr_err', shape=res2a_branch1.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res2a_branch1'] = tf.add(res2a_branch1, err_lyr['res2a_branch1'])
	bn2a_branch1 = batch_normalization(layers_err['res2a_branch1'], scale['bn2a_branch1'], offset['bn2a_branch1'], mean['bn2a_branch1'], variance['bn2a_branch1'])
	res2a_branch2a = conv(pool1, weights_noisy['res2a_branch2a'], biases_noisy['res2a_branch2a'], 1, 1, biased=False, relu=False)
	err_lyr['res2a_branch2a'] = tf.get_variable(name='res2a_branch2a_lyr_err', shape=res2a_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res2a_branch2a'] = tf.add(res2a_branch2a, err_lyr['res2a_branch2a'])
	bn2a_branch2a = batch_normalization(layers_err['res2a_branch2a'], scale['bn2a_branch2a'], offset['bn2a_branch2a'], mean['bn2a_branch2a'], variance['bn2a_branch2a'], relu=True)
	res2a_branch2b = conv(bn2a_branch2a, weights_noisy['res2a_branch2b'], biases_noisy['res2a_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res2a_branch2b'] = tf.get_variable(name='res2a_branch2b_lyr_err', shape=res2a_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res2a_branch2b'] = tf.add(res2a_branch2b, err_lyr['res2a_branch2b'])
	bn2a_branch2b = batch_normalization(layers_err['res2a_branch2b'], scale['bn2a_branch2b'], offset['bn2a_branch2b'], mean['bn2a_branch2b'], variance['bn2a_branch2b'])
	res2a = add([bn2a_branch1, bn2a_branch2b])
	err_lyr['res2a'] = tf.get_variable(name='res2a_lyr_err', shape=res2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res2a'] = tf.add(res2a, err_lyr['res2a'])
	res2a_relu = relu(layers_err['res2a'])
	res2b_branch2a = conv(res2a_relu, weights_noisy['res2b_branch2a'], biases_noisy['res2b_branch2a'], 1, 1, biased=False, relu=False)
	err_lyr['res2b_branch2a'] = tf.get_variable(name='res2b_branch2a_lyr_err', shape=res2b_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res2b_branch2a'] = tf.add(res2b_branch2a, err_lyr['res2b_branch2a'])
	bn2b_branch2a = batch_normalization(layers_err['res2b_branch2a'], scale['bn2b_branch2a'], offset['bn2b_branch2a'], mean['bn2b_branch2a'], variance['bn2b_branch2a'], relu=True)
	res2b_branch2b = conv(bn2b_branch2a, weights_noisy['res2b_branch2b'], biases_noisy['res2b_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res2b_branch2b'] = tf.get_variable(name='res2b_branch2b_lyr_err', shape=res2b_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res2b_branch2b'] = tf.add(res2b_branch2b, err_lyr['res2b_branch2b'])
	bn2b_branch2b = batch_normalization(layers_err['res2b_branch2b'], scale['bn2b_branch2b'], offset['bn2b_branch2b'], mean['bn2b_branch2b'], variance['bn2b_branch2b'])
	res2b = add([res2a_relu, bn2b_branch2b])
	err_lyr['res2b'] = tf.get_variable(name='res2b_lyr_err', shape=res2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res2b'] = tf.add(res2b, err_lyr['res2b'])
	res2b_relu = relu(layers_err['res2b'])
	res3a_branch1 = conv(res2b_relu, weights_noisy['res3a_branch1'], biases_noisy['res3a_branch1'], 2, 2, biased=False, relu=False)
	err_lyr['res3a_branch1'] = tf.get_variable(name='res3a_branch1_lyr_err', shape=res3a_branch1.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res3a_branch1'] = tf.add(res3a_branch1, err_lyr['res3a_branch1'])
	bn3a_branch1 = batch_normalization(layers_err['res3a_branch1'], scale['bn3a_branch1'], offset['bn3a_branch1'], mean['bn3a_branch1'], variance['bn3a_branch1'])
	res3a_branch2a = conv(res2b_relu, weights_noisy['res3a_branch2a'], biases_noisy['res3a_branch2a'], 2, 2, biased=False, relu=False)
	err_lyr['res3a_branch2a'] = tf.get_variable(name='res3a_branch2a_lyr_err', shape=res3a_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res3a_branch2a'] = tf.add(res3a_branch2a, err_lyr['res3a_branch2a'])
	bn3a_branch2a = batch_normalization(layers_err['res3a_branch2a'], scale['bn3a_branch2a'], offset['bn3a_branch2a'], mean['bn3a_branch2a'], variance['bn3a_branch2a'], relu=True)
	res3a_branch2b = conv(bn3a_branch2a, weights_noisy['res3a_branch2b'], biases_noisy['res3a_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res3a_branch2b'] = tf.get_variable(name='res3a_branch2b_lyr_err', shape=res3a_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res3a_branch2b'] = tf.add(res3a_branch2b, err_lyr['res3a_branch2b'])
	bn3a_branch2b = batch_normalization(layers_err['res3a_branch2b'], scale['bn3a_branch2b'], offset['bn3a_branch2b'], mean['bn3a_branch2b'], variance['bn3a_branch2b'])
	res3a = add([bn3a_branch1, bn3a_branch2b])
	err_lyr['res3a'] = tf.get_variable(name='res3a_lyr_err', shape=res3a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res3a'] = tf.add(res3a, err_lyr['res3a'])
	res3a_relu = relu(layers_err['res3a'])
	res3b_branch2a = conv(res3a_relu, weights_noisy['res3b_branch2a'], biases_noisy['res3b_branch2a'], 1, 1, biased=False, relu=False)
	err_lyr['res3b_branch2a'] = tf.get_variable(name='res3b_branch2a_lyr_err', shape=res3b_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res3b_branch2a'] = tf.add(res3b_branch2a, err_lyr['res3b_branch2a'])
	bn3b_branch2a = batch_normalization(layers_err['res3b_branch2a'], scale['bn3b_branch2a'], offset['bn3b_branch2a'], mean['bn3b_branch2a'], variance['bn3b_branch2a'], relu=True)
	res3b_branch2b = conv(bn3b_branch2a, weights_noisy['res3b_branch2b'], biases_noisy['res3b_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res3b_branch2b'] = tf.get_variable(name='res3b_branch2b_lyr_err', shape=res3b_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res3b_branch2b'] = tf.add(res3b_branch2b, err_lyr['res3b_branch2b'])
	bn3b_branch2b = batch_normalization(layers_err['res3b_branch2b'], scale['bn3b_branch2b'], offset['bn3b_branch2b'], mean['bn3b_branch2b'], variance['bn3b_branch2b'])
	res3b = add([res3a_relu, bn3b_branch2b])
	err_lyr['res3b'] = tf.get_variable(name='res3b_lyr_err', shape=res3b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res3b'] = tf.add(res3b, err_lyr['res3b'])
	res3b_relu = relu(layers_err['res3b'])
	res4a_branch1 = conv(res3b_relu, weights_noisy['res4a_branch1'], biases_noisy['res4a_branch1'], 2, 2, biased=False, relu=False)
	err_lyr['res4a_branch1'] = tf.get_variable(name='res4a_branch1_lyr_err', shape=res4a_branch1.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res4a_branch1'] = tf.add(res4a_branch1, err_lyr['res4a_branch1'])
	bn4a_branch1 = batch_normalization(layers_err['res4a_branch1'], scale['bn4a_branch1'], offset['bn4a_branch1'], mean['bn4a_branch1'], variance['bn4a_branch1'])
	res4a_branch2a = conv(res3b_relu, weights_noisy['res4a_branch2a'], biases_noisy['res4a_branch2a'], 2, 2, biased=False, relu=False)
	err_lyr['res4a_branch2a'] = tf.get_variable(name='res4a_branch2a_lyr_err', shape=res4a_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res4a_branch2a'] = tf.add(res4a_branch2a, err_lyr['res4a_branch2a'])
	bn4a_branch2a = batch_normalization(layers_err['res4a_branch2a'], scale['bn4a_branch2a'], offset['bn4a_branch2a'], mean['bn4a_branch2a'], variance['bn4a_branch2a'], relu=True)
	res4a_branch2b = conv(bn4a_branch2a, weights_noisy['res4a_branch2b'], biases_noisy['res4a_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res4a_branch2b'] = tf.get_variable(name='res4a_branch2b_lyr_err', shape=res4a_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res4a_branch2b'] = tf.add(res4a_branch2b, err_lyr['res4a_branch2b'])
	bn4a_branch2b = batch_normalization(layers_err['res4a_branch2b'], scale['bn4a_branch2b'], offset['bn4a_branch2b'], mean['bn4a_branch2b'], variance['bn4a_branch2b'])
	res4a = add([bn4a_branch1, bn4a_branch2b])
	err_lyr['res4a'] = tf.get_variable(name='res4a_lyr_err', shape=res4a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res4a'] = tf.add(res4a, err_lyr['res4a'])
	res4a_relu = relu(layers_err['res4a'])
	res4b_branch2a = conv(res4a_relu, weights_noisy['res4b_branch2a'], biases_noisy['res4b_branch2a'], 1, 1, biased=False, relu=False)
	err_lyr['res4b_branch2a'] = tf.get_variable(name='res4b_branch2a_lyr_err', shape=res4b_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res4b_branch2a'] = tf.add(res4b_branch2a, err_lyr['res4b_branch2a'])
	bn4b_branch2a = batch_normalization(layers_err['res4b_branch2a'], scale['bn4b_branch2a'], offset['bn4b_branch2a'], mean['bn4b_branch2a'], variance['bn4b_branch2a'], relu=True)
	res4b_branch2b = conv(bn4b_branch2a, weights_noisy['res4b_branch2b'], biases_noisy['res4b_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res4b_branch2b'] = tf.get_variable(name='res4b_branch2b_lyr_err', shape=res4b_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res4b_branch2b'] = tf.add(res4b_branch2b, err_lyr['res4b_branch2b'])
	bn4b_branch2b = batch_normalization(layers_err['res4b_branch2b'], scale['bn4b_branch2b'], offset['bn4b_branch2b'], mean['bn4b_branch2b'], variance['bn4b_branch2b'])
	res4b = add([res4a_relu, bn4b_branch2b])
	err_lyr['res4b'] = tf.get_variable(name='res4b_lyr_err', shape=res4b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res4b'] = tf.add(res4b, err_lyr['res4b'])
	res4b_relu = relu(layers_err['res4b'])
	res5a_branch1 = conv(res4b_relu, weights_noisy['res5a_branch1'], biases_noisy['res5a_branch1'], 2, 2, biased=False, relu=False)
	err_lyr['res5a_branch1'] = tf.get_variable(name='res5a_branch1_lyr_err', shape=res5a_branch1.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res5a_branch1'] = tf.add(res5a_branch1, err_lyr['res5a_branch1'])
	bn5a_branch1 = batch_normalization(layers_err['res5a_branch1'], scale['bn5a_branch1'], offset['bn5a_branch1'], mean['bn5a_branch1'], variance['bn5a_branch1'])
	res5a_branch2a = conv(res4b_relu, weights_noisy['res5a_branch2a'], biases_noisy['res5a_branch2a'], 2, 2, biased=False, relu=False)
	err_lyr['res5a_branch2a'] = tf.get_variable(name='res5a_branch2a_lyr_err', shape=res5a_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res5a_branch2a'] = tf.add(res5a_branch2a, err_lyr['res5a_branch2a'])
	bn5a_branch2a = batch_normalization(layers_err['res5a_branch2a'], scale['bn5a_branch2a'], offset['bn5a_branch2a'], mean['bn5a_branch2a'], variance['bn5a_branch2a'], relu=True)
	res5a_branch2b = conv(bn5a_branch2a, weights_noisy['res5a_branch2b'], biases_noisy['res5a_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res5a_branch2b'] = tf.get_variable(name='res5a_branch2b_lyr_err', shape=res5a_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res5a_branch2b'] = tf.add(res5a_branch2b, err_lyr['res5a_branch2b'])
	bn5a_branch2b = batch_normalization(layers_err['res5a_branch2b'], scale['bn5a_branch2b'], offset['bn5a_branch2b'], mean['bn5a_branch2b'], variance['bn5a_branch2b'])
	res5a = add([bn5a_branch1, bn5a_branch2b])
	err_lyr['res5a'] = tf.get_variable(name='res5a_lyr_err', shape=res5a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res5a'] = tf.add(res5a, err_lyr['res5a'])
	res5a_relu = relu(layers_err['res5a'])
	res5b_branch2a = conv(res5a_relu, weights_noisy['res5b_branch2a'], biases_noisy['res5b_branch2a'], 1, 1, biased=False, relu=False)
	err_lyr['res5b_branch2a'] = tf.get_variable(name='res5b_branch2a_lyr_err', shape=res5b_branch2a.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res5b_branch2a'] = tf.add(res5b_branch2a, err_lyr['res5b_branch2a'])
	bn5b_branch2a = batch_normalization(layers_err['res5b_branch2a'], scale['bn5b_branch2a'], offset['bn5b_branch2a'], mean['bn5b_branch2a'], variance['bn5b_branch2a'], relu=True)
	res5b_branch2b = conv(bn5b_branch2a, weights_noisy['res5b_branch2b'], biases_noisy['res5b_branch2b'], 1, 1, biased=False, relu=False)
	err_lyr['res5b_branch2b'] = tf.get_variable(name='res5b_branch2b_lyr_err', shape=res5b_branch2b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res5b_branch2b'] = tf.add(res5b_branch2b, err_lyr['res5b_branch2b'])
	bn5b_branch2b = batch_normalization(layers_err['res5b_branch2b'], scale['bn5b_branch2b'], offset['bn5b_branch2b'], mean['bn5b_branch2b'], variance['bn5b_branch2b'])
	res5b = add([res5a_relu, bn5b_branch2b])
	err_lyr['res5b'] = tf.get_variable(name='res5b_lyr_err', shape=res5b.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['res5b'] = tf.add(res5b, err_lyr['res5b'])
	res5b_relu = relu(layers_err['res5b'])
	pool5 = avg_pool(res5b_relu, 7, 7, 1, 1, padding='VALID')
	fc1000 = fc(pool5, weights_noisy['fc1000'], biases_noisy['fc1000'], relu=False)
	err_lyr['fc1000'] = tf.get_variable(name='fc1000_lyr_err', shape=fc1000.shape[1:], initializer=tf.random_normal_initializer(mean=err_mean[3], stddev=err_stddev[3]), trainable=train_vars[3])
	layers_err['fc1000'] = tf.add(fc1000, err_lyr['fc1000'])
	return layers_err['fc1000'], err_w, err_b, err_lyr

def resnet18(input_node, netparams):
	weights, biases = netparams['weights'], netparams['biases']
	mean, variance, scale, offset = netparams['mean'], netparams['variance'], netparams['scale'], netparams['offset']
	#data_spec = helper.get_data_spec('resnet18')
	data_spec = get_data_spec('resnet18')
	conv1 = conv(input_node, weights['conv1'], biases['conv1'], 2, 2, biased=False, relu=False)
	bn_conv1 = batch_normalization(conv1, scale['bn_conv1'], offset['bn_conv1'], mean['bn_conv1'], variance['bn_conv1'], relu=True)
	pool1 = max_pool(bn_conv1, 3, 3, 2, 2)
	res2a_branch1 = conv(pool1, weights['res2a_branch1'], biases['res2a_branch1'], 1, 1, biased=False, relu=False)
	bn2a_branch1 = batch_normalization(res2a_branch1, scale['bn2a_branch1'], offset['bn2a_branch1'], mean['bn2a_branch1'], variance['bn2a_branch1'], )
	res2a_branch2a = conv(pool1, weights['res2a_branch2a'], biases['res2a_branch2a'], 1, 1, biased=False, relu=False)
	bn2a_branch2a = batch_normalization(res2a_branch2a, scale['bn2a_branch2a'], offset['bn2a_branch2a'], mean['bn2a_branch2a'], variance['bn2a_branch2a'], relu=True)
	res2a_branch2b = conv(bn2a_branch2a, weights['res2a_branch2b'], biases['res2a_branch2b'], 1, 1, biased=False, relu=False)
	bn2a_branch2b = batch_normalization(res2a_branch2b, scale['bn2a_branch2b'], offset['bn2a_branch2b'], mean['bn2a_branch2b'], variance['bn2a_branch2b'], )
	res2a = add([bn2a_branch1, bn2a_branch2b])
	res2a_relu = relu(res2a)
	res2b_branch2a = conv(res2a_relu, weights['res2b_branch2a'], biases['res2b_branch2a'], 1, 1, biased=False, relu=False)
	bn2b_branch2a = batch_normalization(res2b_branch2a, scale['bn2b_branch2a'], offset['bn2b_branch2a'], mean['bn2b_branch2a'], variance['bn2b_branch2a'], relu=True)
	res2b_branch2b = conv(bn2b_branch2a, weights['res2b_branch2b'], biases['res2b_branch2b'], 1, 1, biased=False, relu=False)
	bn2b_branch2b = batch_normalization(res2b_branch2b, scale['bn2b_branch2b'], offset['bn2b_branch2b'], mean['bn2b_branch2b'], variance['bn2b_branch2b'], )
	res2b = add([res2a_relu, bn2b_branch2b])
	res2b_relu = relu(res2b)
	res3a_branch1 = conv(res2b_relu, weights['res3a_branch1'], biases['res3a_branch1'], 2, 2, biased=False, relu=False)
	bn3a_branch1 = batch_normalization(res3a_branch1, scale['bn3a_branch1'], offset['bn3a_branch1'], mean['bn3a_branch1'], variance['bn3a_branch1'], )
	res3a_branch2a = conv(res2b_relu, weights['res3a_branch2a'], biases['res3a_branch2a'], 2, 2, biased=False, relu=False)
	bn3a_branch2a = batch_normalization(res3a_branch2a, scale['bn3a_branch2a'], offset['bn3a_branch2a'], mean['bn3a_branch2a'], variance['bn3a_branch2a'], relu=True)
	res3a_branch2b = conv(bn3a_branch2a, weights['res3a_branch2b'], biases['res3a_branch2b'], 1, 1, biased=False, relu=False)
	bn3a_branch2b = batch_normalization(res3a_branch2b, scale['bn3a_branch2b'], offset['bn3a_branch2b'], mean['bn3a_branch2b'], variance['bn3a_branch2b'], )
	res3a = add([bn3a_branch1, bn3a_branch2b])
	res3a_relu = relu(res3a)
	res3b_branch2a = conv(res3a_relu, weights['res3b_branch2a'], biases['res3b_branch2a'], 1, 1, biased=False, relu=False)
	bn3b_branch2a = batch_normalization(res3b_branch2a, scale['bn3b_branch2a'], offset['bn3b_branch2a'], mean['bn3b_branch2a'], variance['bn3b_branch2a'], relu=True)
	res3b_branch2b = conv(bn3b_branch2a, weights['res3b_branch2b'], biases['res3b_branch2b'], 1, 1, biased=False, relu=False)
	bn3b_branch2b = batch_normalization(res3b_branch2b, scale['bn3b_branch2b'], offset['bn3b_branch2b'], mean['bn3b_branch2b'], variance['bn3b_branch2b'], )
	res3b = add([res3a_relu, bn3b_branch2b])
	res3b_relu = relu(res3b)
	res4a_branch1 = conv(res3b_relu, weights['res4a_branch1'], biases['res4a_branch1'], 2, 2, biased=False, relu=False)
	bn4a_branch1 = batch_normalization(res4a_branch1, scale['bn4a_branch1'], offset['bn4a_branch1'], mean['bn4a_branch1'], variance['bn4a_branch1'], )
	res4a_branch2a = conv(res3b_relu, weights['res4a_branch2a'], biases['res4a_branch2a'], 2, 2, biased=False, relu=False)
	bn4a_branch2a = batch_normalization(res4a_branch2a, scale['bn4a_branch2a'], offset['bn4a_branch2a'], mean['bn4a_branch2a'], variance['bn4a_branch2a'], relu=True)
	res4a_branch2b = conv(bn4a_branch2a, weights['res4a_branch2b'], biases['res4a_branch2b'], 1, 1, biased=False, relu=False)
	bn4a_branch2b = batch_normalization(res4a_branch2b, scale['bn4a_branch2b'], offset['bn4a_branch2b'], mean['bn4a_branch2b'], variance['bn4a_branch2b'], )
	res4a = add([bn4a_branch1, bn4a_branch2b])
	res4a_relu = relu(res4a)
	res4b_branch2a = conv(res4a_relu, weights['res4b_branch2a'], biases['res4b_branch2a'], 1, 1, biased=False, relu=False)
	bn4b_branch2a = batch_normalization(res4b_branch2a, scale['bn4b_branch2a'], offset['bn4b_branch2a'], mean['bn4b_branch2a'], variance['bn4b_branch2a'], relu=True)
	res4b_branch2b = conv(bn4b_branch2a, weights['res4b_branch2b'], biases['res4b_branch2b'], 1, 1, biased=False, relu=False)
	bn4b_branch2b = batch_normalization(res4b_branch2b, scale['bn4b_branch2b'], offset['bn4b_branch2b'], mean['bn4b_branch2b'], variance['bn4b_branch2b'], )
	res4b = add([res4a_relu, bn4b_branch2b])
	res4b_relu = relu(res4b)
	res5a_branch1 = conv(res4b_relu, weights['res5a_branch1'], biases['res5a_branch1'], 2, 2, biased=False, relu=False)
	bn5a_branch1 = batch_normalization(res5a_branch1, scale['bn5a_branch1'], offset['bn5a_branch1'], mean['bn5a_branch1'], variance['bn5a_branch1'], )
	res5a_branch2a = conv(res4b_relu, weights['res5a_branch2a'], biases['res5a_branch2a'], 2, 2, biased=False, relu=False)
	bn5a_branch2a = batch_normalization(res5a_branch2a, scale['bn5a_branch2a'], offset['bn5a_branch2a'], mean['bn5a_branch2a'], variance['bn5a_branch2a'], relu=True)
	res5a_branch2b = conv(bn5a_branch2a, weights['res5a_branch2b'], biases['res5a_branch2b'], 1, 1, biased=False, relu=False)
	bn5a_branch2b = batch_normalization(res5a_branch2b, scale['bn5a_branch2b'], offset['bn5a_branch2b'], mean['bn5a_branch2b'], variance['bn5a_branch2b'], )
	res5a = add([bn5a_branch1, bn5a_branch2b])
	res5a_relu = relu(res5a)
	res5b_branch2a = conv(res5a_relu, weights['res5b_branch2a'], biases['res5b_branch2a'], 1, 1, biased=False, relu=False)
	bn5b_branch2a = batch_normalization(res5b_branch2a, scale['bn5b_branch2a'], offset['bn5b_branch2a'], mean['bn5b_branch2a'], variance['bn5b_branch2a'], relu=True)
	res5b_branch2b = conv(bn5b_branch2a, weights['res5b_branch2b'], biases['res5b_branch2b'], 1, 1, biased=False, relu=False)
	bn5b_branch2b = batch_normalization(res5b_branch2b, scale['bn5b_branch2b'], offset['bn5b_branch2b'], mean['bn5b_branch2b'], variance['bn5b_branch2b'], )
	res5b = add([res5a_relu, bn5b_branch2b])
	res5b_relu = relu(res5b)
	pool5 = avg_pool(res5b_relu, 7, 7, 1, 1, padding='VALID')
	fc1000 = fc(pool5, weights['fc1000'], biases['fc1000'], relu=False)
	return fc1000


def resnet18_shift(input_node, netparams, shift_back):
	layer_shift={}
	weights, biases = netparams['weights'], netparams['biases']
	mean, variance, scale, offset = netparams['mean'], netparams['variance'], netparams['scale'], netparams['offset']
	#data_spec = helper.get_data_spec('resnet18')
	data_spec = get_data_spec('resnet18')
	conv1 = conv(input_node, weights['conv1'], biases['conv1'], 2, 2, biased=False, relu=False)
	bn_conv1 = batch_normalization(conv1, scale['bn_conv1'], offset['bn_conv1'], mean['bn_conv1'], variance['bn_conv1'], relu=True)
	pool1 = max_pool(bn_conv1, 3, 3, 2, 2)
	res2a_branch1 = conv(pool1, weights['res2a_branch1'], biases['res2a_branch1'], 1, 1, biased=False, relu=False)
	layer_shift['res2a_branch1'] = tf.divide(res2a_branch1, 2**shift_back['res2a_branch1'])
	
	bn2a_branch1 = batch_normalization(layer_shift['res2a_branch1'], scale['bn2a_branch1'], offset['bn2a_branch1'], mean['bn2a_branch1'], variance['bn2a_branch1'], )
	res2a_branch2a = conv(pool1, weights['res2a_branch2a'], biases['res2a_branch2a'], 1, 1, biased=False, relu=False)
	layer_shift['res2a_branch2a'] = tf.divide(res2a_branch2a, 2**shift_back['res2a_branch2a'])
	
	bn2a_branch2a = batch_normalization(layer_shift['res2a_branch2a'], scale['bn2a_branch2a'], offset['bn2a_branch2a'], mean['bn2a_branch2a'], variance['bn2a_branch2a'], relu=True)
	#bn2a_branch2a = batch_normalization(res2a_branch2a, scale['bn2a_branch2a'], offset['bn2a_branch2a'], mean['bn2a_branch2a'], variance['bn2a_branch2a'], relu=True)
	res2a_branch2b = conv(bn2a_branch2a, weights['res2a_branch2b'], biases['res2a_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res2a_branch2b'] = tf.divide(res2a_branch2b, 2**shift_back['res2a_branch2b'])

	bn2a_branch2b = batch_normalization(layer_shift['res2a_branch2b'], scale['bn2a_branch2b'], offset['bn2a_branch2b'], mean['bn2a_branch2b'], variance['bn2a_branch2b'], )
	res2a = add([bn2a_branch1, bn2a_branch2b])
	res2a_relu = relu(res2a)
	res2b_branch2a = conv(res2a_relu, weights['res2b_branch2a'], biases['res2b_branch2a'], 1, 1, biased=False, relu=False)
	layer_shift['res2b_branch2a'] = tf.divide(res2b_branch2a, 2**shift_back['res2b_branch2a'])

	bn2b_branch2a = batch_normalization(layer_shift['res2b_branch2a'], scale['bn2b_branch2a'], offset['bn2b_branch2a'], mean['bn2b_branch2a'], variance['bn2b_branch2a'], relu=True)
	res2b_branch2b = conv(bn2b_branch2a, weights['res2b_branch2b'], biases['res2b_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res2b_branch2b'] = tf.divide(res2b_branch2b, 2**shift_back['res2b_branch2b'])

	bn2b_branch2b = batch_normalization(layer_shift['res2b_branch2b'], scale['bn2b_branch2b'], offset['bn2b_branch2b'], mean['bn2b_branch2b'], variance['bn2b_branch2b'], )
	res2b = add([res2a_relu, bn2b_branch2b])
	res2b_relu = relu(res2b)
	res3a_branch1 = conv(res2b_relu, weights['res3a_branch1'], biases['res3a_branch1'], 2, 2, biased=False, relu=False)
	layer_shift['res3a_branch1'] = tf.divide(res3a_branch1, 2**shift_back['res3a_branch1'])

	bn3a_branch1 = batch_normalization(layer_shift['res3a_branch1'], scale['bn3a_branch1'], offset['bn3a_branch1'], mean['bn3a_branch1'], variance['bn3a_branch1'], )
	res3a_branch2a = conv(res2b_relu, weights['res3a_branch2a'], biases['res3a_branch2a'], 2, 2, biased=False, relu=False)
	layer_shift['res3a_branch2a'] = tf.divide(res3a_branch2a, 2**shift_back['res3a_branch2a'])

	bn3a_branch2a = batch_normalization(layer_shift['res3a_branch2a'], scale['bn3a_branch2a'], offset['bn3a_branch2a'], mean['bn3a_branch2a'], variance['bn3a_branch2a'], relu=True)
	res3a_branch2b = conv(bn3a_branch2a, weights['res3a_branch2b'], biases['res3a_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res3a_branch2b'] = tf.divide(res3a_branch2b, 2**shift_back['res3a_branch2b'])

	bn3a_branch2b = batch_normalization(layer_shift['res3a_branch2b'], scale['bn3a_branch2b'], offset['bn3a_branch2b'], mean['bn3a_branch2b'], variance['bn3a_branch2b'], )
	res3a = add([bn3a_branch1, bn3a_branch2b])
	res3a_relu = relu(res3a)
	res3b_branch2a = conv(res3a_relu, weights['res3b_branch2a'], biases['res3b_branch2a'], 1, 1, biased=False, relu=False)
	layer_shift['res3b_branch2a'] = tf.divide(res3b_branch2a, 2**shift_back['res3b_branch2a'])

	bn3b_branch2a = batch_normalization(layer_shift['res3b_branch2a'], scale['bn3b_branch2a'], offset['bn3b_branch2a'], mean['bn3b_branch2a'], variance['bn3b_branch2a'], relu=True)
	res3b_branch2b = conv(bn3b_branch2a, weights['res3b_branch2b'], biases['res3b_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res3b_branch2b'] = tf.divide(res3b_branch2b, 2**shift_back['res3b_branch2b'])
	
	bn3b_branch2b = batch_normalization(layer_shift['res3b_branch2b'], scale['bn3b_branch2b'], offset['bn3b_branch2b'], mean['bn3b_branch2b'], variance['bn3b_branch2b'], )
	res3b = add([res3a_relu, bn3b_branch2b])
	res3b_relu = relu(res3b)
	res4a_branch1 = conv(res3b_relu, weights['res4a_branch1'], biases['res4a_branch1'], 2, 2, biased=False, relu=False)
	layer_shift['res4a_branch1'] = tf.divide(res4a_branch1, 2**shift_back['res4a_branch1'])
	
	bn4a_branch1 = batch_normalization(layer_shift['res4a_branch1'], scale['bn4a_branch1'], offset['bn4a_branch1'], mean['bn4a_branch1'], variance['bn4a_branch1'], )
	res4a_branch2a = conv(res3b_relu, weights['res4a_branch2a'], biases['res4a_branch2a'], 2, 2, biased=False, relu=False)
	layer_shift['res4a_branch2a'] = tf.divide(res4a_branch2a, 2**shift_back['res4a_branch2a'])
	
	bn4a_branch2a = batch_normalization(layer_shift['res4a_branch2a'], scale['bn4a_branch2a'], offset['bn4a_branch2a'], mean['bn4a_branch2a'], variance['bn4a_branch2a'], relu=True)
	res4a_branch2b = conv(bn4a_branch2a, weights['res4a_branch2b'], biases['res4a_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res4a_branch2b'] = tf.divide(res4a_branch2b, 2**shift_back['res4a_branch2b'])
	
	bn4a_branch2b = batch_normalization(layer_shift['res4a_branch2b'], scale['bn4a_branch2b'], offset['bn4a_branch2b'], mean['bn4a_branch2b'], variance['bn4a_branch2b'], )
	res4a = add([bn4a_branch1, bn4a_branch2b])
	res4a_relu = relu(res4a)
	res4b_branch2a = conv(res4a_relu, weights['res4b_branch2a'], biases['res4b_branch2a'], 1, 1, biased=False, relu=False)
	layer_shift['res4b_branch2a'] = tf.divide(res4b_branch2a, 2**shift_back['res4b_branch2a'])
	
	bn4b_branch2a = batch_normalization(layer_shift['res4b_branch2a'], scale['bn4b_branch2a'], offset['bn4b_branch2a'], mean['bn4b_branch2a'], variance['bn4b_branch2a'], relu=True)
	res4b_branch2b = conv(bn4b_branch2a, weights['res4b_branch2b'], biases['res4b_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res4b_branch2b'] = tf.divide(res4b_branch2b, 2**shift_back['res4b_branch2b'])
	
	bn4b_branch2b = batch_normalization(layer_shift['res4b_branch2b'], scale['bn4b_branch2b'], offset['bn4b_branch2b'], mean['bn4b_branch2b'], variance['bn4b_branch2b'], )
	res4b = add([res4a_relu, bn4b_branch2b])
	res4b_relu = relu(res4b)
	res5a_branch1 = conv(res4b_relu, weights['res5a_branch1'], biases['res5a_branch1'], 2, 2, biased=False, relu=False)
	layer_shift['res5a_branch1'] = tf.divide(res5a_branch1, 2**shift_back['res5a_branch1'])
	
	bn5a_branch1 = batch_normalization(layer_shift['res5a_branch1'], scale['bn5a_branch1'], offset['bn5a_branch1'], mean['bn5a_branch1'], variance['bn5a_branch1'], )
	res5a_branch2a = conv(res4b_relu, weights['res5a_branch2a'], biases['res5a_branch2a'], 2, 2, biased=False, relu=False)
	layer_shift['res5a_branch2a'] = tf.divide(res5a_branch2a, 2**shift_back['res5a_branch2a'])
	
	bn5a_branch2a = batch_normalization(layer_shift['res5a_branch2a'], scale['bn5a_branch2a'], offset['bn5a_branch2a'], mean['bn5a_branch2a'], variance['bn5a_branch2a'], relu=True)
	res5a_branch2b = conv(bn5a_branch2a, weights['res5a_branch2b'], biases['res5a_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res5a_branch2b'] = tf.divide(res5a_branch2b, 2**shift_back['res5a_branch2b'])
	
	bn5a_branch2b = batch_normalization(layer_shift['res5a_branch2b'], scale['bn5a_branch2b'], offset['bn5a_branch2b'], mean['bn5a_branch2b'], variance['bn5a_branch2b'], )
	res5a = add([bn5a_branch1, bn5a_branch2b])
	res5a_relu = relu(res5a)
	res5b_branch2a = conv(res5a_relu, weights['res5b_branch2a'], biases['res5b_branch2a'], 1, 1, biased=False, relu=False)
	layer_shift['res5b_branch2a'] = tf.divide(res5b_branch2a, 2**shift_back['res5b_branch2a'])
	
	bn5b_branch2a = batch_normalization(layer_shift['res5b_branch2a'], scale['bn5b_branch2a'], offset['bn5b_branch2a'], mean['bn5b_branch2a'], variance['bn5b_branch2a'], relu=True)
	res5b_branch2b = conv(bn5b_branch2a, weights['res5b_branch2b'], biases['res5b_branch2b'], 1, 1, biased=False, relu=False)
	layer_shift['res5b_branch2b'] = tf.divide(res5b_branch2b, 2**shift_back['res5b_branch2b'])
	
	bn5b_branch2b = batch_normalization(layer_shift['res5b_branch2b'], scale['bn5b_branch2b'], offset['bn5b_branch2b'], mean['bn5b_branch2b'], variance['bn5b_branch2b'], )
	res5b = add([res5a_relu, bn5b_branch2b])
	res5b_relu = relu(res5b)
	pool5 = avg_pool(res5b_relu, 7, 7, 1, 1, padding='VALID')
	fc1000 = fc(pool5, weights['fc1000'], biases['fc1000'], relu=False)
	layer_shift['fc1000'] = tf.divide(fc1000, 2**shift_back['fc1000'])
	
	return layer_shift['fc1000']


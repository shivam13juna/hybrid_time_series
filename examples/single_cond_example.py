import numpy as np
import tensorflow as tf

from cond_rnn import ConditionalRNN

NUM_SAMPLES = 10_000
INPUT_DIM = 1
NUM_CLASSES = 3
TIME_STEPS = 10
NUM_CELLS = 12


def create_conditions():
    conditions = np.zeros(shape=[NUM_SAMPLES, NUM_CLASSES]) 
    for i, kk in enumerate(conditions):
        kk[i % NUM_CLASSES] = 1
    return conditions


def main():
    class MySimpleModel(tf.keras.Model):
        def __init__(self):
            super(MySimpleModel, self).__init__()
            self.cond = ConditionalRNN(NUM_CELLS, cell='LSTM', dtype=tf.float32)
            self.out = tf.keras.layers.Dense(units=NUM_CLASSES, activation='softmax')

        def call(self, inputs, **kwargs):
            o = self.cond(inputs)
            o = self.out(o)
            return o

    model = MySimpleModel()

    # Define (real) data.
    train_inputs = np.random.uniform(size=(NUM_SAMPLES, TIME_STEPS, INPUT_DIM))
    test_inputs = np.random.uniform(size=(NUM_SAMPLES, TIME_STEPS, INPUT_DIM))
    test_targets = train_targets = create_conditions()

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.1)
    model.call([train_inputs, train_targets])
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=[train_inputs, train_targets], y=train_targets,
              validation_data=([test_inputs, test_targets], test_targets),
              epochs=10)

    te_loss, te_acc = model.evaluate([test_inputs, test_targets], test_targets)
    assert abs(te_acc - 1) < 1e-5


if __name__ == '__main__':
    main()


# Acha, so supposedly I've a time-series dataset, and some non-sequential data. For example
# in weather forecasting i've data of temperature which are sequential data, but then I also have 
# non-sequential data, for example City. and I've to make a model for predicting weather, 
# you think it make sense to append non-sequential data with sequential ones and pass it through LSTM


# Problem in above case would be that I'd be polluting sequentail data with non-sequential ones. 


# Other approach is that I pass non-sequential data through some dense layer then append it with 
# lstm output and then pass the appended data through some dense layers. You think this approach would 
# be better? 
import numpy as np
import pandas as pd

from .models import Attribute, BuildingClass, ClassAttribute

# The observations dataframe should have at least the following columns:
#   class_id: same as building_classes class_id (string, unique)
#   count: number of observations of this class (int, positive)
#   [attribute]: number of observations of this attribute for a given class_id (integer)
DEFAULT_OBSERVATIONS = pd.DataFrame({'class_id': ['0110', '0111', '0112'],
                                     '1': [1, 1, 1],
                                     '101': [1, 0, 1],
                                     '102': [0, 1, 0]})


def calculate_conditional_probabilities(observations):
    '''Calculates the conditional probability table from the building observations and returns them as a Pandas dataframe'''
    # Start with building_observations
    df = observations.copy()

    # Find attribute columns
    attribute_cols = df.columns[(
        df.columns != 'class_id') & (df.columns != 'count')]

    # Convert the observation values into probabilities with Laplace smoothing
    df[attribute_cols] = (df[attribute_cols] + 1) / 3

    return df


class NaiveBayesClassifier:
    def __init__(self, app=None):
        # Save app in order to connect to database for loading data
        self.app = app

        # Default empty dataframes for conditional probabilities
        self.conditional_probabilities = pd.DataFrame(
            columns=['class_id', 'count'])  # FIXME: remove count

        # Empty prior
        self.prior = np.array(())

    def load_from_db(self):
        with self.app.app_context():
            # Load prior
            building_classes = BuildingClass.query.order_by('class_id').all()
            self.prior = np.array(
                [x.class_probability for x in building_classes])

            # Load attribute default probabilities
            attributes = Attribute.query.order_by('attribute_id').all()
            data = {x.attribute_id: x.probability for x in attributes}
            data['class_id'] = [x.class_id for x in building_classes]
            self.conditional_probabilities = pd.DataFrame(data)

            # Complement or override conditional probabilities
            class_attributes = ClassAttribute.query.all()
            for x in class_attributes:
                # No need to change anything if the class-attribute pair is normal
                if x.class_has_attribute and x.custom_probability is None:
                    continue

                # If the class doesn't have the attribute, the new probability is the complement
                if not x.class_has_attribute and x.custom_probability is None:
                    new_prob = 1 - x.attribute.probability

                # If a custom probability is provided, that is the new probability
                if x.custom_probability is not None:
                    new_prob = x.custom_probability

                # Replace the corresponding entry in the conditional probability table
                attribute_id = x.attribute.attribute_id
                mask = self.conditional_probabilities.class_id == x.building_class.class_id
                self.conditional_probabilities.loc[mask,
                                                   attribute_id] = new_prob

    # def load_from_file(self, observation_file):
    #    try:
    #        observations = load_observations(observation_file)
    #    except ValueError as error:
    #        print(
    #            f'Unable to load observations ({observation_file}): {error.args[0]}')
    #        observations = DEFAULT_OBSERVATIONS
    #    self.conditional_probabilities = calculate_conditional_probabilities(
    #        observations)

    #    # Assume uniform prior
    #    self.prior = np.ones(observations.shape[0])

    def calculate_posterior(self, attribute, value, prior=None, normalize=True):
        '''Calculates the posterior probability for each building class given attribute and value'''
        if isinstance(attribute, str):
            raise ValueError(
                'calculate_posterior(): You must provide attribute as a list or tuple of strings, not a string')
        if isinstance(value, str):
            raise ValueError(
                'calculate_posterior(): You must provide the value as a list or tuple of strings, not a string')

        prior_probability = prior
        posterior = None
        # Use default prior, if none is provided
        if prior_probability is None:
            prior_probability = self.prior

        # Extract the likelihood from the conditional probability table
        for (val, attr) in zip(value, attribute):
            if val == 'yes':
                likelihood = self.conditional_probabilities[attr]
            elif val == 'no':
                likelihood = 1 - self.conditional_probabilities[attr]
            else:
                likelihood = 1

            # Calculate the posterior and normalize if requested
            posterior = prior_probability * likelihood

            if normalize:
                posterior /= posterior.sum()
            prior_probability = posterior

        # Create Pandas dataframe with building class and posterior
        df = pd.DataFrame({'class_id': self.conditional_probabilities.class_id,
                           'posterior': posterior})
        return df

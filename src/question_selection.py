import numpy as np
import pandas as pd
import src
from .models import db, QuestionGroup, Attribute


def best_questions(prior, answered_questions):
    '''Returns attribute with lowest resultant entropy of posteriors'''

    # Find the attributes that can be asked
    free_attributes = [x['attribute_id'] for x in src.building_data.attribute.values() if
                       x['active'] == True and
                       x['attribute_id'] not in answered_questions and
                       x['attribute_id'] in src.classifier.conditional_probabilities.columns]

    # Get the conditional probability table and the prior
    cond_p = src.classifier.conditional_probabilities[free_attributes]
    prior = prior if prior is not None else np.ones(
        cond_p.shape[0]) / cond_p.shape[0]

    # Calculate and normalize posteriors for yes and no answers
    p_yes = cond_p * prior[:, None]
    p_yes /= p_yes.sum(axis=0)
    p_no = (1 - cond_p) * prior[:, None]
    p_no /= p_no.sum(axis=0)

    # Calculate entropy
    entropy = -(p_yes * np.log(p_yes)).sum(axis=0) - \
        (p_no * np.log(p_no)).sum(axis=0)
    entropy = entropy.sort_values()
    entropy = [(i, x) for i, x in zip(entropy.index, entropy)]

    return entropy


def next_question(prior, answered_questions):
    '''Returns best question to be asked next'''

    best = best_questions(prior, answered_questions)
    if best:
        ident = best[0][0]
        attribute = src.building_data.attribute[ident]

        # Checks if attribute is part of a group:
        if attribute['group_id'] is not None:
            groups = src.building_data.attribute_groups
            attributes = src.building_data.attribute.values()
            group = groups.loc[groups['group_id'] == attribute['group_id']]
            selected = [x for x in attributes if x['group_id']
                        == attribute['group_id']]
            new_attributes = [{'attribute_id': x['attribute_id'],
                               'attribute_name': x['attribute_name'],
                               'attribute_tooltip': x['attribute_tooltip']} for x in selected]  # FIXME: is this needed?
            group_question = None

            if len(group['group_question']) > 0:
                group_question = group['group_question'].values[0]

            group = {
                'type': 'multi',
                'attribute_question': group_question,
                'attributes': new_attributes
            }
            return group
        else:
            question = {
                'type': 'simple',
                'attribute_id': attribute['attribute_id'],
                'attribute_name': attribute['attribute_name'],
                'attribute_question': attribute['attribute_question'],
                'attribute_tooltip': attribute['attribute_tooltip']
            }
            return question
    else:
        # All questions asked
        return {'type': 'none', 'attribute_id': '', 'attribute_name': '', 'attribute_question': '', 'attribute_tooltip': ''}

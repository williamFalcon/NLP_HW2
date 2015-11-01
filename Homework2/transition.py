class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # word in stack cannot be a dependency. Also, cannot be root
        idx_last_stack = conf.stack[-1]
        is_root = (idx_last_stack is 0)
        precond_met = (not Transition.is_index_dependent(idx_last_stack, conf.arcs)) and not is_root

        if not precond_met:
            return -1

        # do left arc
        conf.stack.pop(-1)

        # get first thing in buffer
        idx_first_buffer = conf.buffer[0]

        # create the arch dependency
        conf.arcs.append((idx_first_buffer, relation, idx_last_stack))


    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        # return -1 if buffer or stack are empty/null
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1] # get last item in stack
        idx_wj = conf.buffer.pop(0) # get first thing in buffer

        conf.stack.append(idx_wj) # add thing just popped from buffer
        conf.arcs.append((idx_wi, relation, idx_wj)) # create the arch dependency

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        # return -1 if buffer or stack are empty/null
        if not conf.buffer or not conf.stack:
            return -1

        # pointer to item to examine
        idx_last_stack = conf.stack[-1]

        # pre condition, last item on stack must be a dependant of something (must be on the right of a relation
        precond_met = Transition.is_index_dependent(idx_last_stack, conf.arcs)

        # conduct reduce
        if precond_met:
            conf.stack.pop(-1)
        else:
            return -1

    @staticmethod
    def is_index_dependent(index, arcs):
        """
        Determines if the given index is already a dependent in the arcs passed in
        :param index:
        :param arcs:
        :return:
        """
        is_dep = False

        # see if item is a dep
        for arc in arcs:
            parent, relation, child = arc
            if child is index:
                is_dep = True
                break

        return is_dep


    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
        # return -1 if buffer or stack are empty/null
        if not conf.buffer:
            return -1

        # push first item of buffer into stack
        conf.stack.append(conf.buffer.pop(0))

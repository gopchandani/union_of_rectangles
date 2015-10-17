__author__ = 'Rakesh Kumar'

class SegmentTreeNode:

    def __init__(self, l, r):

        self.l = l
        self.r = r

        self.lc = None
        self.rc = None

        # TODO: Attributes at this node as a dict
        # General attributes/properties
        self.C = 0

        # Specific to measure problem
        self.m = 0

        # Specific to perimeter problem
        self.lbd = 0
        self.rbd = 0
        self.alpha = 0

        # Specific to contour problem
        self.status = 'empty'

    def insert(self, left, right):
        if left <= self.l and self.r <= right:
            self.C += 1
        else:
            if left < (self.l + self.r) / 2:
                self.lc.insert(left, right)
            if (self.l + self.r) / 2 < right:
                self.rc.insert(left, right)

        self.update()

    def delete(self, left, right):
        if left <= self.l and self.r <= right:
            self.C -= 1
        else:
            if left < (self.l + self.r) / 2:
                self.lc.delete(left, right)
            if (self.l + self.r) / 2 < right:
                self.rc.delete(left, right)

        self.update()

    def update(self):

        # Update m
        if self.C != 0:
            self.m = self.r - self.l
        else:
            if (self.lc and self.rc):
                self.m = self.lc.m + self.rc.m
            else:
                self.m = 0

        # Update lbd, rbd and alpha
        if self.C > 0:
            self.alpha = 2
            self.lbd = 1
            self.rbd = 1
        else:
            if self.lc and self.rc:
                self.alpha = self.lc.alpha + self.rc.alpha - 2 * self.lc.rbd * self.rc.lbd
                self.lbd = self.lc.lbd
                self.rbd = self.rc.rbd
            else:
                self.alpha = 0
                self.lbd = 0
                self.rbd = 0

        # Update status
        if self.C > 0:
            self.status = 'full'
        else:
            if self.lc and self.rc:
                if self.lc.status == 'empty' and self.rc.status == 'empty':
                    self.status = 'empty'
                else:
                    self.status = 'partial'
            else:
                self.status = 'empty'

    # For contours, this computes the contribution of a given vertex
    def contr(self, left, right, stack):

        if self.status != 'full':

            if (left <= self.l and self.r <= right) and (self.status == 'empty'):
                if stack and self.l == stack[len(stack) - 1]:
                    stack.pop()
                else:
                    stack.append(self.l)
                stack.append(self.r)
            else:

                if self.lc and self.rc:
                    if left < (self.l + self.r) / 2:
                        self.lc.contr(left, right, stack)
                    if (self.l + self.r) / 2 < right:
                        self.rc.contr(left, right, stack)

class SegmentTree:

    def __init__(self, neg_inf, pos_inf):

        self.neg_inf = neg_inf
        self.pos_inf = pos_inf

        self.root = self.build_seg_tree(self.neg_inf, self.pos_inf)

    def build_seg_tree(self, l, r):

        subtree = SegmentTreeNode(l, r)

        if r - l > 1:
            subtree.lc = self.build_seg_tree(l, (l + r)/2)
            subtree.rc = self.build_seg_tree((l + r)/2, r)

        return subtree
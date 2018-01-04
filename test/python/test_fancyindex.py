#!/usr/bin/env python

import unittest
import numpy
import ctf


def allclose(a, b):
    return abs(ctf.to_nparray(a) - ctf.to_nparray(b)).sum() < 1e-14

class KnowValues(unittest.TestCase):
    def test__getitem__(self):
        a0 = numpy.arange(12.).reshape(4,3)
        a1 = ctf.astensor(a0)
        self.assertTrue(allclose(a1[3], a0[3]))
        self.assertEqual(a1[(3,1)], a1[3,1])
        self.assertTrue(a1[1:3:2].shape == (1,3))
        self.assertTrue(a1[:,1:].shape == (4,2))
        self.assertTrue(a1[:,:1].shape == (4,1))
        self.assertTrue(allclose(a1[[3,1]], a0[[3,1]]))
        self.assertTrue(allclose(a1[:,[2,1]], a0[:,[2,1]]))
        self.assertTrue(allclose(a1[1:3,2:3], a0[1:3,2:3]))
        self.assertTrue(allclose(a1[1:3,2:5], a0[1:3,2:3]))
        self.assertTrue(allclose(a1[1:-2], a0[1:-2]))
        with self.assertRaises(IndexError):
            a1[[3,4]]

        a0 = numpy.arange(60.).reshape(5,4,3)
        a1 = ctf.astensor(a0)
        self.assertTrue(allclose(a1[1:3,:,2:], a0[1:3,:,2:]))

#    def test_fancyindex(self):
#        a0 = numpy.arange(60.).reshape(5,4,3)
#        a1 = ctf.astensor(a0)
#        idx = numpy.arange(3)
#        self.assertTrue(a1[idx,idx,:].shape == (3, 3))
#        self.assertTrue(a1[:,idx,idx].shape == (5, 3))
#        self.assertTrue(a1[idx,:,idx].shape == (3, 4))
#        self.assertTrue(allclose(a1[idx,idx+1,:], a0[idx,idx+1,:]))

    def test__getitem__(self):
        a0 = numpy.arange(12.).reshape(4,3)
        a1 = ctf.astensor(a0)
        self.assertTrue(a1.shape == (4,3))
        self.assertTrue(a1[1].shape == (3,))

    def test__setitem__(self):
        def a0_and_a1():
            a0 = numpy.arange(60.).reshape(5,4,3)
            a1 = ctf.astensor(a0)
            return a0, a1
        a0, a1 = a0_and_a1()
        a1[3] = 99
        a0[3] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[3] = a0[3] + 11
        a0[3] += 11
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[(3,1)] = 99
        a0[3,1] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[(3,1)] = a0[3,1] + 11
        a0[3,1] += 11
        self.assertTrue(allclose(a1, a0))

        a1[1:3:2] = 99
        a0[1:3:2] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[:,1:] = 99
        a0[:,1:] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[:,:1] = 99
        a0[:,:1] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[:,:1] = a0[:,:1] + 11
        a0[:,:1] += 11
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[[3,1]] = 99
        a0[[3,1]] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[:,[2,1]] = 99
        a0[:,[2,1]] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[1:3,2:3] = 99
        a0[1:3,2:3] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[1:3,2:5] = 99
        a0[1:3,2:5] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[1:3,2:5] = a0[1:3,2:5] + 11
        a0[1:3,2:5] += 11
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[1:-2] = 99
        a0[1:-2] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[1:3,:,2:] = 99
        a0[1:3,:,2:] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[1:3,:,2:] = a0[1:3,:,2:] + 11
        a0[1:3,:,2:] += 11
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        a1[...,1] = 99
        a0[...,1] = 99
        self.assertTrue(allclose(a1, a0))

        with self.assertRaises(IndexError):
            a1[[3,6]] = 99

        with self.assertRaises(ValueError):  # shape mismatch error
            a1[[2,3]] = a1

# Some advanced fancy indices which involve multiple dimensions of a tensor.
# Remove these tests if they are not compatible to the distributed tensor
# structure.
        idx = numpy.array([1,2,3])
        idy = numpy.array([0,2])
        a0, a1 = a0_and_a1()
        a1[idx[:,None],idy] = 99
        a0[idx[:,None],idy] = 99
        self.assertTrue(allclose(a1, a0))
        a0, a1 = a0_and_a1()
        a1[idx[:,None],:,idy] = 99
        a0[idx[:,None],:,idy] = 99
        self.assertTrue(allclose(a1, a0))
        a0, a1 = a0_and_a1()
        a1[:,idx[:,None],idy] = 99
        a0[:,idx[:,None],idy] = 99
        self.assertTrue(allclose(a1, a0))
        a0, a1 = a0_and_a1()
        a1[idx[:,None,None],idy[:,None],idy] = 99
        a0[idx[:,None,None],idy[:,None],idy] = 99
        self.assertTrue(allclose(a1, a0))

        bidx = numpy.zeros(5, dtype=bool)
        bidy = numpy.zeros(4, dtype=bool)
        bidz = numpy.zeros(3, dtype=bool)
        bidx[idx] = True
        bidy[idy] = True
        bidz[idy] = True
        a0, a1 = a0_and_a1()
        a1[bidx] = 99
        a0[bidx] = 99
        self.assertTrue(allclose(a1, a0))
        a0, a1 = a0_and_a1()
        a1[:,bidy] = 99
        a0[:,bidy] = 99
        self.assertTrue(allclose(a1, a0))
        a0, a1 = a0_and_a1()
        a1[:,:,bidz] = 99
        a0[:,:,bidz] = 99
        self.assertTrue(allclose(a1, a0))

        a0, a1 = a0_and_a1()
        mask = bidx[:,None] & bidy
        a1[mask] = 99
        a0[mask] = 99
        self.assertTrue(allclose(a1, a0))
        a0, a1 = a0_and_a1()
        mask = bidy[:,None] & bidz
        a1[:,mask] = 99
        a0[:,mask] = 99
        self.assertTrue(allclose(a1, a0))
        a0, a1 = a0_and_a1()
        mask = bidy[:,None] & bidz
        a1[:,mask] = 99
        a0[:,mask] = 99
        self.assertTrue(allclose(a1, a0))


    def test__getslice__(self):
        a0 = ctf.astensor(numpy.arange(12.).reshape(4,3))
        self.assertTrue(a0[1:].shape == (3,3))

    def test__setslice__(self):
        a0 = ctf.astensor(numpy.arange(12.).reshape(4,3))
        a0[1:3] = 9


if __name__ == "__main__":
    print("Tests for fancy index")
    unittest.main()


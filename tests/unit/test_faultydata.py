"""
Unit tests for faulty data sets.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest

import ga4gh.datamodel.datasets as datasets
import ga4gh.datamodel.references as references
import ga4gh.datamodel.variants as variants
import ga4gh.exceptions as exceptions
import ga4gh.protocol as protocol


class FaultyVariantDataTest(unittest.TestCase):
    def setUp(self):
        self.testDataDir = "tests/faultydata/variants"
        self.dataset = datasets.AbstractDataset('dataset1')

    def getFullPath(self, localId):
        return os.path.join(self.testDataDir, localId)


class TestVariantSetNoIndexedVcf(FaultyVariantDataTest):
    setIds = ["no_indexed_vcf"]

    def testInstantiation(self):
        for localId in self.setIds:
            path = self.getFullPath(localId)
            self.assertRaises(
                exceptions.NotIndexedException,
                variants.HtslibVariantSet, self.dataset, localId, path)


class TestInconsistentMetaData(FaultyVariantDataTest):
    setIds = ["inconsist_meta"]

    def testInstantiation(self):
        for localId in self.setIds:
            path = self.getFullPath(localId)
            with self.assertRaises(exceptions.InconsistentMetaDataException):
                variants.HtslibVariantSet(self.dataset, localId, path)


class TestInconsistentCallSetId(FaultyVariantDataTest):
    setIds = ["inconsist_sampleid", "inconsist_sampleid2"]

    def testInstantiation(self):
        for localId in self.setIds:
            path = self.getFullPath(localId)
            with self.assertRaises(exceptions.InconsistentCallSetIdException):
                variants.HtslibVariantSet(self.dataset, localId, path)


class TestOverlappingVcfVariants(FaultyVariantDataTest):
    setIds = ["overlapping_vcf"]

    def testInstantiation(self):
        for localId in self.setIds:
            path = self.getFullPath(localId)
            with self.assertRaises(exceptions.OverlappingVcfException):
                variants.HtslibVariantSet(self.dataset, localId, path)


class TestEmptyDirException(FaultyVariantDataTest):
    setIds = ["empty_dir"]

    def testInstantiation(self):
        for localId in self.setIds:
            path = self.getFullPath(localId)
            self.assertRaises(
                exceptions.EmptyDirException,
                variants.HtslibVariantSet, self.dataset, localId, path)


class TestDuplicateCallSetId(FaultyVariantDataTest):
    """
    THIS SECTION IS CURRENTLY NOT WORKING
    It returns the following error:

    [E::bcf_hdr_add_sample] Duplicated sample name 'S1'
    Aborted (core dumped)

    which is coming from:
    htslib/vcf.c function bcf_hdr_add_sample

    UNABLE TO CAPTURE EXCEPTION
    """
    setIds = ["duplicated_sampleid"]

    @unittest.skipIf(protocol.version.startswith("0.6"), "")
    def testInstantiation(self):
        for localId in self.setIds:
            path = self.getFullPath(localId)
            self.assertRaises(
                exceptions.DuplicateCallSetIdException,
                variants.HtslibVariantSet, self.dataset, localId, path)


class FaultyReferenceDataTest(unittest.TestCase):
    def setUp(self):
        self.testDataDir = "tests/faultydata/references"

    def getFullPath(self, referenceSetId):
        return os.path.join(self.testDataDir, referenceSetId)


class TestTwoReferences(FaultyReferenceDataTest):
    setIds = ["two_references"]

    def testInstantiation(self):
        for referenceSetId in self.setIds:
            path = self.getFullPath(referenceSetId)
            with self.assertRaises(exceptions.NotExactlyOneReferenceException):
                references.HtslibReferenceSet(referenceSetId, path)

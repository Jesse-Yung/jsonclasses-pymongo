from __future__ import annotations
import unittest
from typing import List, Dict
from dotenv import load_dotenv
from datetime import date, datetime
from bson import ObjectId
from jsonclasses import jsonclass, types
from jsonclasses_pymongo import MongoObject
from jsonclasses_pymongo.decoder import Decoder

class TestDecoder(unittest.TestCase):

  def test_decode_str_into_str(self):
    @jsonclass
    class SimpleDecodeStr(MongoObject):
      val1: str
      val2: str
    data = {
      '_id': ObjectId(),
      'createdAt': datetime.now(),
      'updatedAt': datetime.now(),
      'val1': '12345',
      'val2': '67890'
    }
    instance = Decoder().decode_root(data, SimpleDecodeStr)
    self.assertEqual(instance.id, str(data['_id']))
    self.assertEqual(instance.val1, '12345')
    self.assertEqual(instance.val2, '67890')
    self.assertIsInstance(instance.val1, str)
    self.assertIsInstance(instance.val2, str)

  def test_decode_int_into_int(self):
    @jsonclass
    class SimpleDecodeInt(MongoObject):
      val1: int
      val2: int
    data = {
      '_id': ObjectId(),
      'createdAt': datetime.now(),
      'updatedAt': datetime.now(),
      'val1': 12345,
      'val2': 67890
    }
    instance = Decoder().decode_root(data, SimpleDecodeInt)
    self.assertEqual(instance.id, str(data['_id']))
    self.assertEqual(instance.val1, 12345)
    self.assertEqual(instance.val2, 67890)

  def test_decode_float_into_float(self):
    @jsonclass
    class SimpleDecodeFloat(MongoObject):
      val1: float
      val2: float
    data = {
      '_id': ObjectId(),
      'createdAt': datetime.now(),
      'updatedAt': datetime.now(),
      'val1': 12345.6,
      'val2': 67890.1
    }
    instance = Decoder().decode_root(data, SimpleDecodeFloat)
    self.assertEqual(instance.id, str(data['_id']))
    self.assertEqual(instance.val1, 12345.6)
    self.assertEqual(instance.val2, 67890.1)

  def test_decode_bool_into_bool(self):
    @jsonclass
    class SimpleDecodeBool(MongoObject):
      val1: bool
      val2: bool
    data = {
      '_id': ObjectId(),
      'createdAt': datetime.now(),
      'updatedAt': datetime.now(),
      'val1': True,
      'val2': False
    }
    instance = Decoder().decode_root(data, SimpleDecodeBool)
    self.assertEqual(instance.id, str(data['_id']))
    self.assertEqual(instance.val1, True)
    self.assertEqual(instance.val2, False)

  def test_decode_datetime_into_date(self):
    @jsonclass
    class SimpleDecodeDate(MongoObject):
      val1: date
      val2: date
    data = {
      '_id': ObjectId(),
      'createdAt': datetime.now(),
      'updatedAt': datetime.now(),
      'val1': datetime(2012, 9, 5, 0, 0, 0),
      'val2': datetime(2020, 9, 5, 0, 0, 0),
    }
    instance = Decoder().decode_root(data, SimpleDecodeDate)
    self.assertEqual(instance.id, str(data['_id']))
    self.assertEqual(instance.val1, date(2012, 9, 5))
    self.assertEqual(instance.val2, date(2020, 9, 5))

  def test_decode_datetime_into_datetime(self):
    @jsonclass
    class SimpleDecodeDatetime(MongoObject):
      val1: datetime
      val2: datetime
    data = {
      '_id': ObjectId(),
      'createdAt': datetime.now(),
      'updatedAt': datetime.now(),
      'val1': datetime(2012, 9, 5, 6, 25, 0),
      'val2': datetime(2020, 9, 5, 8, 25, 0),
    }
    instance = Decoder().decode_root(data, SimpleDecodeDatetime)
    self.assertEqual(instance.id, str(data['_id']))
    self.assertEqual(instance.val1, datetime(2012, 9, 5, 6, 25, 0))
    self.assertEqual(instance.val2, datetime(2020, 9, 5, 8, 25, 0))

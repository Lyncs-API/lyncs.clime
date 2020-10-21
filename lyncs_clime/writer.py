"""
Writer functions for lime files
"""
# pylint: disable=C0303

__all__ = [
    "Writer",
]

import sys
import os
from array import array
from .lib import lib
from .status import check_status

class Writer:

    # TODO
    """
    DOCSTRING
    """
    
    def __init__(self, filename):
        # TODO: FINISH THIS 
        """
        Writer to a lime file
        
        Parameters
        ----------
        filename: str
           Name of the file
        """
        assert (not os.path.isfile(filename))
        self.filename = os.path.abspath(filename)
        self._fp = None
        self._writer = None
        self._bstart = 0

    def __del__(self):
        if self.isopen:
            self.close()

    @property
    def writer(self):
        "The c-lime writer"
        if not self.isopen:
            self.open()
        return self._writer

    @property
    def isopen(self):
        "Returns if the file is open"
        return self._writer is not None
    
    def open(self):
        "Opens the file writer"
        self._fp = lib.fopen(self.filename, "w")
        self._writer = lib.limeCreateWriter(self._fp)

    def close(self):
        "Closes the file writer"
        if not self.isopen:
            raise RuntimeError("File needs to be open first")

        lib.limeDestroyWriter(self.writer)
        lib.fclose(self._fp)
        self._fp = None
        self._writer = None
        self._buffstart = 0
        
    def _write(self, record, rtype):
        "Writes a single record to the file
        MB_flag = 1; ME_flag = 1; bytes = sys.getsizeof(record)
        h = lib.limeCreateHeader( MB_flag, ME_flag, rtype, bytes  )
        status = lib.limeWriteRecordHeader( h, self.writer )
        if status < 0:
            raise RuntimeError("Error encountered while writing header of record")
        lib.limeDestroyHeader(h)
        
        status = lib.limeWriteRecordData( self._buffstart, bytes, self.writer );
        if status != self.LIME_SUCCESS:
            raise RuntimeError("Error encountered while writing record")
        self._buffstart += bytes
        
        
        
    def write(self, records, record_types):
        """
        Writes records to the file
        
        Parameters
        ----------
        records: list of strings
            Records to be written
        record_types: list of strings
            Types of each record        
        """
        if len(records) != len(record_types):
            raise ValueError("Length mismatch record list of length {} but types of length {}".format(len(records),len(record_types))
        if not self.isopen:
            self.open()
        for record, rtype in enumerate( zip(records,record_types) ):
            self._write(record, rtype)

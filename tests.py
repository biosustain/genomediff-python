from unittest import TestCase
from io import StringIO

from genomediff import Metadata, GenomeDiff
from genomediff.parser import GenomeDiffParser
from genomediff.records import Record


class ParserTestCase(TestCase):
    def test_parse(self):
        file = StringIO("""
#=GENOME_DIFF	1.0
#=AUTHOR test
SNP	1	23423	NC_000913	223	A	gene_name=mhpE
RA	2		NC_000913	223	0	G	A	frequency=0.1366
                        """.strip())
        p = GenomeDiffParser(fsock=file)
        self.assertEqual([
                             Metadata('GENOME_DIFF', '1.0'),
                             Metadata('AUTHOR', 'test'),
                             Record('SNP', 1, parent_ids=[23423], new_seq='A', seq_id='NC_000913', position=223, gene_name='mhpE'),
                             Record('RA', 2, new_base='A', frequency=0.1366, position=223, seq_id='NC_000913',
                                    insert_position=0,
                                    ref_base='G')],
                         list(p)
        )


class GenomeDiffTestCase(TestCase):
    def test_document(self):
        file = StringIO("""
#=GENOME_DIFF	1.0
#=AUTHOR test
SNP	1	23423	NC_000913	223	A
RA	2		NC_000913	223	0	G	A
                        """.strip())

        document = GenomeDiff.read(file)

        self.assertEqual({'AUTHOR': 'test', 'GENOME_DIFF': '1.0'}, document.metadata)

        snp_record = Record('SNP', 1, document, [23423], seq_id='NC_000913', new_seq='A', position=223)
        ra_record = Record('RA', 2, document, None, position=223, seq_id='NC_000913', insert_position=0, new_base='A',
                           ref_base='G')

        self.assertEqual([snp_record], document.mutations)
        self.assertEqual([ra_record], document.evidence)
        self.assertEqual(snp_record, document[1])
        self.assertEqual(ra_record, document[2])


class RecordTestCase(TestCase):
    def test_simple(self):
        snp_record = Record('SNP', 1, parent_ids=[23423], seq_id='NC_000913', new_seq='A', position=223, test='more')

        self.assertEqual('SNP', snp_record.type)
        self.assertEqual(1, snp_record.id)
        self.assertEqual('A', snp_record.new_seq)
        self.assertEqual('more', snp_record.test)


class ParentResolveTestCase(TestCase):
    def test_resolve(self):
        file = StringIO("""
#=GENOME_DIFF	1.0
#=AUTHOR test
SNP	1	2	NC_000913	223	A
RA	2		NC_000913	223	0	G	A
                        """.strip())
        document = GenomeDiff.read(file)
        self.assertEqual(document[1].parents, [document[2]])
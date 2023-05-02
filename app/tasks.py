import subprocess

from background_task import background
from django.conf import settings

from .models import BlastSearchResult, GeneBlastFastaType, BlastSearchResultStatus


@background(schedule=0)
def run_blast_analysis(result_id):
    result_obj = BlastSearchResult.objects.filter(id=result_id).first()

    if result_obj is not None:
        _args = []
        if result_obj.fasta_type == GeneBlastFastaType.NUCLEOTIDE:
            _args += [settings.NCBI_BLAST_NUCL_PATH, "-db", settings.NUCL_BLASTDB_PATH]
        else:
            _args += [settings.NCBI_BLAST_PROT_PATH, "-db", settings.PROT_BLASTDB_PATH]

        _args += ["-query", result_obj.query_fasta.path]

        result_args = [*_args, "-outfmt", "0", "-out", result_obj.result_file.path, "-num_threads", "4"]
        json_output_args = [*_args, "-outfmt", "15", "-out", result_obj.result_json_file.path, "-num_threads", "4"]
        
        print(f"Result id: {result_id}", " ".join(result_args))
        subprocess.run(args=result_args, check=True)

        print(f"Result id: {result_id}", " ".join(json_output_args))
        subprocess.run(args=json_output_args, check=True)
        result_obj.status = BlastSearchResultStatus.COMPLETED
        result_obj.save()

# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import proto  # type: ignore


from google.cloud.video.transcoder_v1beta1.types import resources


__protobuf__ = proto.module(
    package="google.cloud.video.transcoder.v1beta1",
    manifest={
        "CreateJobRequest",
        "ListJobsRequest",
        "GetJobRequest",
        "DeleteJobRequest",
        "ListJobsResponse",
        "CreateJobTemplateRequest",
        "ListJobTemplatesRequest",
        "GetJobTemplateRequest",
        "DeleteJobTemplateRequest",
        "ListJobTemplatesResponse",
    },
)


class CreateJobRequest(proto.Message):
    r"""Request message for ``TranscoderService.CreateJob``.

    Attributes:
        parent (str):
            Required. The parent location to create and process this
            job. Format: ``projects/{project}/locations/{location}``
        job (~.resources.Job):
            Required. Parameters for creating transcoding
            job.
    """

    parent = proto.Field(proto.STRING, number=1)

    job = proto.Field(proto.MESSAGE, number=2, message=resources.Job,)


class ListJobsRequest(proto.Message):
    r"""Request message for ``TranscoderService.ListJobs``. The parent
    location from which to retrieve the collection of jobs.

    Attributes:
        parent (str):
            Required. Format:
            ``projects/{project}/locations/{location}``
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The ``next_page_token`` value returned from a previous List
            request, if any.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class GetJobRequest(proto.Message):
    r"""Request message for ``TranscoderService.GetJob``.

    Attributes:
        name (str):
            Required. The name of the job to retrieve. Format:
            ``projects/{project}/locations/{location}/jobs/{job}``
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteJobRequest(proto.Message):
    r"""Request message for ``TranscoderService.DeleteJob``.

    Attributes:
        name (str):
            Required. The name of the job to delete. Format:
            ``projects/{project}/locations/{location}/jobs/{job}``
    """

    name = proto.Field(proto.STRING, number=1)


class ListJobsResponse(proto.Message):
    r"""Response message for ``TranscoderService.ListJobs``.

    Attributes:
        jobs (Sequence[~.resources.Job]):
            List of jobs in the specified region.
        next_page_token (str):
            The pagination token.
    """

    @property
    def raw_page(self):
        return self

    jobs = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.Job,)

    next_page_token = proto.Field(proto.STRING, number=2)


class CreateJobTemplateRequest(proto.Message):
    r"""Request message for ``TranscoderService.CreateJobTemplate``.

    Attributes:
        parent (str):
            Required. The parent location to create this job template.
            Format: ``projects/{project}/locations/{location}``
        job_template (~.resources.JobTemplate):
            Required. Parameters for creating job
            template.
        job_template_id (str):
            Required. The ID to use for the job template, which will
            become the final component of the job template's resource
            name.

            This value should be 4-63 characters, and valid characters
            are ``/[a-zA-Z0-9_-_]/``.
    """

    parent = proto.Field(proto.STRING, number=1)

    job_template = proto.Field(proto.MESSAGE, number=2, message=resources.JobTemplate,)

    job_template_id = proto.Field(proto.STRING, number=3)


class ListJobTemplatesRequest(proto.Message):
    r"""Request message for ``TranscoderService.ListJobTemplates``.

    Attributes:
        parent (str):
            Required. The parent location from which to retrieve the
            collection of job templates. Format:
            ``projects/{project}/locations/{location}``
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The ``next_page_token`` value returned from a previous List
            request, if any.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class GetJobTemplateRequest(proto.Message):
    r"""Request message for ``TranscoderService.GetJobTemplate``.

    Attributes:
        name (str):
            Required. The name of the job template to retrieve. Format:
            ``projects/{project}/locations/{location}/jobTemplates/{job_template}``
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteJobTemplateRequest(proto.Message):
    r"""Request message for ``TranscoderService.DeleteJobTemplate``.

    Attributes:
        name (str):
            Required. The name of the job template to delete.
            ``projects/{project}/locations/{location}/jobTemplates/{job_template}``
    """

    name = proto.Field(proto.STRING, number=1)


class ListJobTemplatesResponse(proto.Message):
    r"""Response message for ``TranscoderService.ListJobTemplates``.

    Attributes:
        job_templates (Sequence[~.resources.JobTemplate]):
            List of job templates in the specified
            region.
        next_page_token (str):
            The pagination token.
    """

    @property
    def raw_page(self):
        return self

    job_templates = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.JobTemplate,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
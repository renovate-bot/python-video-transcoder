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

from collections import OrderedDict
import os
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.video.transcoder_v1beta1.services.transcoder_service import pagers
from google.cloud.video.transcoder_v1beta1.types import resources
from google.cloud.video.transcoder_v1beta1.types import services

from .transports.base import TranscoderServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import TranscoderServiceGrpcTransport
from .transports.grpc_asyncio import TranscoderServiceGrpcAsyncIOTransport


class TranscoderServiceClientMeta(type):
    """Metaclass for the TranscoderService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[TranscoderServiceTransport]]
    _transport_registry["grpc"] = TranscoderServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = TranscoderServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[TranscoderServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class TranscoderServiceClient(metaclass=TranscoderServiceClientMeta):
    """Using the Transcoder API, you can queue asynchronous jobs for
    transcoding media into various output formats. Output formats
    may include different streaming standards such as HTTP Live
    Streaming (HLS) and Dynamic Adaptive Streaming over HTTP (DASH).
    You can also customize jobs using advanced features such as
    Digital Rights Management (DRM), audio equalization, content
    concatenation, and digital ad-stitch ready content generation.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "transcoder.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def job_path(project: str, location: str, job: str,) -> str:
        """Return a fully-qualified job string."""
        return "projects/{project}/locations/{location}/jobs/{job}".format(
            project=project, location=location, job=job,
        )

    @staticmethod
    def parse_job_path(path: str) -> Dict[str, str]:
        """Parse a job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/jobs/(?P<job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def job_template_path(project: str, location: str, job_template: str,) -> str:
        """Return a fully-qualified job_template string."""
        return "projects/{project}/locations/{location}/jobTemplates/{job_template}".format(
            project=project, location=location, job_template=job_template,
        )

    @staticmethod
    def parse_job_template_path(path: str) -> Dict[str, str]:
        """Parse a job_template path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/jobTemplates/(?P<job_template>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, TranscoderServiceTransport] = None,
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transcoder service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TranscoderServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, TranscoderServiceTransport):
            # transport is a TranscoderServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_job(
        self,
        request: services.CreateJobRequest = None,
        *,
        parent: str = None,
        job: resources.Job = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Job:
        r"""Creates a job in the specified region.

        Args:
            request (:class:`~.services.CreateJobRequest`):
                The request object. Request message for
                `TranscoderService.CreateJob`.
            parent (:class:`str`):
                Required. The parent location to create and process this
                job. Format: ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (:class:`~.resources.Job`):
                Required. Parameters for creating
                transcoding job.
                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Job:
                Transcoding job resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.CreateJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.CreateJobRequest):
            request = services.CreateJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if job is not None:
                request.job = job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_jobs(
        self,
        request: services.ListJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobsPager:
        r"""Lists jobs in the specified region.

        Args:
            request (:class:`~.services.ListJobsRequest`):
                The request object. Request message for
                `TranscoderService.ListJobs`. The parent location from
                which to retrieve the collection of jobs.
            parent (:class:`str`):
                Required. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListJobsPager:
                Response message for ``TranscoderService.ListJobs``.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.ListJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.ListJobsRequest):
            request = services.ListJobsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_job(
        self,
        request: services.GetJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Job:
        r"""Returns the job data.

        Args:
            request (:class:`~.services.GetJobRequest`):
                The request object. Request message for
                `TranscoderService.GetJob`.
            name (:class:`str`):
                Required. The name of the job to retrieve. Format:
                ``projects/{project}/locations/{location}/jobs/{job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.Job:
                Transcoding job resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.GetJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.GetJobRequest):
            request = services.GetJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_job(
        self,
        request: services.DeleteJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job.

        Args:
            request (:class:`~.services.DeleteJobRequest`):
                The request object. Request message for
                `TranscoderService.DeleteJob`.
            name (:class:`str`):
                Required. The name of the job to delete. Format:
                ``projects/{project}/locations/{location}/jobs/{job}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.DeleteJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.DeleteJobRequest):
            request = services.DeleteJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_job_template(
        self,
        request: services.CreateJobTemplateRequest = None,
        *,
        parent: str = None,
        job_template: resources.JobTemplate = None,
        job_template_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.JobTemplate:
        r"""Creates a job template in the specified region.

        Args:
            request (:class:`~.services.CreateJobTemplateRequest`):
                The request object. Request message for
                `TranscoderService.CreateJobTemplate`.
            parent (:class:`str`):
                Required. The parent location to create this job
                template. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_template (:class:`~.resources.JobTemplate`):
                Required. Parameters for creating job
                template.
                This corresponds to the ``job_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_template_id (:class:`str`):
                Required. The ID to use for the job template, which will
                become the final component of the job template's
                resource name.

                This value should be 4-63 characters, and valid
                characters are ``/[a-zA-Z0-9_-_]/``.
                This corresponds to the ``job_template_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.JobTemplate:
                Transcoding job template resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, job_template, job_template_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.CreateJobTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.CreateJobTemplateRequest):
            request = services.CreateJobTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if job_template is not None:
                request.job_template = job_template
            if job_template_id is not None:
                request.job_template_id = job_template_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_job_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_job_templates(
        self,
        request: services.ListJobTemplatesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobTemplatesPager:
        r"""Lists job templates in the specified region.

        Args:
            request (:class:`~.services.ListJobTemplatesRequest`):
                The request object. Request message for
                `TranscoderService.ListJobTemplates`.
            parent (:class:`str`):
                Required. The parent location from which to retrieve the
                collection of job templates. Format:
                ``projects/{project}/locations/{location}``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListJobTemplatesPager:
                Response message for
                ``TranscoderService.ListJobTemplates``.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.ListJobTemplatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.ListJobTemplatesRequest):
            request = services.ListJobTemplatesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_job_templates]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListJobTemplatesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_job_template(
        self,
        request: services.GetJobTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.JobTemplate:
        r"""Returns the job template data.

        Args:
            request (:class:`~.services.GetJobTemplateRequest`):
                The request object. Request message for
                `TranscoderService.GetJobTemplate`.
            name (:class:`str`):
                Required. The name of the job template to retrieve.
                Format:
                ``projects/{project}/locations/{location}/jobTemplates/{job_template}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.resources.JobTemplate:
                Transcoding job template resource.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.GetJobTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.GetJobTemplateRequest):
            request = services.GetJobTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_job_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_job_template(
        self,
        request: services.DeleteJobTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job template.

        Args:
            request (:class:`~.services.DeleteJobTemplateRequest`):
                The request object. Request message for
                `TranscoderService.DeleteJobTemplate`.
            name (:class:`str`):
                Required. The name of the job template to delete.
                ``projects/{project}/locations/{location}/jobTemplates/{job_template}``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a services.DeleteJobTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, services.DeleteJobTemplateRequest):
            request = services.DeleteJobTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_job_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-video-transcoder",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TranscoderServiceClient",)

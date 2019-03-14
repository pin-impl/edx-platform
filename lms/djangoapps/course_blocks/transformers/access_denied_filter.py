"""
Hide Empty Transformer implementation.
"""
# TODO: Remove this file after REVE-52 lands and old-mobile-app traffic falls to < 5% of mobile traffic
from openedx.core.djangoapps.content.block_structure.transformer import (
    BlockStructureTransformer
)


class AccessDeniedMessageFilterTransformer(BlockStructureTransformer):
    """
    A transformer that removes any block from the course that has an
    authorization_denial_reason or an authorization_denial_message.
    """
    WRITE_VERSION = 1
    READ_VERSION = 1

    @classmethod
    def name(cls):
        """
        Unique identifier for the transformer's class;
        same identifier used in setup.py.
        """
        return "access_denied_message_filter"

    @classmethod
    def collect(cls, block_structure):
        """
        Collects any information that's necessary to execute this
        transformer's transform method.
        """
        block_structure.request_xblock_fields('authorization_denial_reason', 'authorization_denial_message')

    def transform(self, usage_info, block_structure):
        def _filter(block_key):
            has_children = block_structure.get_xblock_field(block_key, 'has_children')
            children = block_structure.get_xblock_field(block_key, 'children')
            return has_children and not any(child in block_structure for child in children)

        for _ in block_structure.post_order_traversal(
            filter_func=block_structure.create_removal_filter(_filter)
        ):
            pass

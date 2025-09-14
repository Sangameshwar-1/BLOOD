from mongoengine import Document, DateTimeField, StringField
from datetime import datetime, timezone


class TimestampedDocument(Document):
    """
    Base document class that automatically tracks creation and update timestamps.
    Also provides optional user tracking fields.
    """
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    created_by = StringField()  # Optional: can be set by view logic to track who created the record
    updated_by = StringField()  # Optional: can be set by view logic to track who updated the record
    
    meta = {'abstract': True}  # This makes it an abstract base class
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically update the updated_at timestamp
        and set created_at only on first save.
        """
        # Only set created_at if this is a new document (no _id yet)
        if not self.pk:
            self.created_at = datetime.now(timezone.utc)
        
        # Always update the updated_at timestamp
        self.updated_at = datetime.now(timezone.utc)
        
        return super(TimestampedDocument, self).save(*args, **kwargs)
    
    def get_timestamp_fields(self):
        """
        Helper method to get timestamp fields for JSON serialization.
        Returns a dictionary with timestamp fields formatted as ISO strings.
        """
        timestamp_data = {}
        if self.created_at:
            timestamp_data['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            timestamp_data['updated_at'] = self.updated_at.isoformat()
        if self.created_by:
            timestamp_data['created_by'] = self.created_by
        if self.updated_by:
            timestamp_data['updated_by'] = self.updated_by
        return timestamp_data